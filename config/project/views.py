from django.shortcuts import render
# django rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response

# django
from django.shortcuts import get_object_or_404
from django.db.models import Q

# core apps
from .serializers import * 
from .models import * 

# auth
from authentication.models import User

import json

from .utils import *


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.update_funcs = {
            'song' : self.__song__,
            'status' : self.__status__,
        }

    def create(self, request):


        params = request.query_params
        user = get_object_or_404(User, pk = params['user_id'])
        project = Project(
            leader = user,
            title = params['title'],
            content = params['content'],
        )
        project.save()
        project = ProjectSerializer(project)
        return Response(project.data, status=status.HTTP_200_OK)

    def list(self, request):
        params = request.query_params

        query_set = self.queryset.filter(
            # Q(author__id = params['user_id']) |
            # Q(songs__players__id__contains = params['user_id'])
        ).distinct(
        ).order_by('-create_date')
        
        # serialize
        serializer = ProjectSerializer(data=query_set, many = True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return self.update_funcs[request.query_params['action']](request, *args, **kwargs)

        

    # ----- update functions ----- #
    def __song__(self, request, *args, **kwargs):
        params = request.query_params

        instance = get_object_or_404(Project, pk = params['project_id'])
        # 필요한 것은 song id, fixed여부. 일단 효율은 둘째치고 받았다. 
        
        selected = [s['id'] for s in json.loads(params['selectedSongs']) if s['fix']]
        not_selected = [s['id'] for s in json.loads(params['selectedSongs']) if not s['fix']]

        instance.songs.filter(
            Q(id__in = selected)
        ).update(fix = True)
        instance.songs.filter(
            Q(id__in = not_selected)
        ).update(fix = False)

        instance.save()

        return Response(None, status= status.HTTP_200_OK)   

    def __status__(self, request, *args, **kwargs):
        params = request.query_params
        instance = get_object_or_404(Project, pk = params['project_id'])
        instance.status = params['status']
        instance.save()
        return Response(None, status= status.HTTP_200_OK)   

   

    # def retrieve(self, request, pk=None):
    #     project = get_object_or_404(Project, pk = request.parser_context['kwargs']['pk'])
    #     print("retrieve")
    #     return Response(ProjectSerializer(project).data)

    # def destroy(self, request, pk=None):
    #     primary_key = request.parser_context['kwargs']['pk']
    #     project = get_object_or_404(Project, pk = primary_key)
    #     project.delete()

    #     return Response({}, status= status.HTTP_200_OK)

class SongViewSet(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    permission_classes = [IsAuthenticated]


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.update_funcs = {
            'apply' : self.__apply__,
            'quit' : self.__quit__,
            'fix' : self.__fix__,
        }

    def create(self, request):
        params = request.query_params
        positions = parsePosition(json.loads(params['positions']))
        user = get_object_or_404(User, pk = params['user_id'])
        project = get_object_or_404(Project, pk = params['project_id'])
        song = Song(
            author = user,
            title = params['title'],
            artist = params['artist'],
            content = params['content'],
            instruments = positions,
            project = project
        )
        song.save()
        song = SongSerializer(song)
        return Response(song.data, status=status.HTTP_200_OK)

    def list(self, request):
        params = request.query_params
        query_set = self.queryset.filter(
            Q(project__id = params['project_id'])
        ).order_by('-create_date')

        # serialize
        serializer = SongSerializer(data=query_set, many = True)
        serializer.is_valid()

        for song in serializer.data:
            print("#-----------------------#")
            print(song['title'])
            print("#-----------------------#")

            for player in song['players']:
                print(player['player']['user']['name'], player['fixed'])


        # allPlayers = instance.players.all()

        # selected = allPlayers.filter(Q(id__in = players))
        # notselected = allPlayers.exclude(Q(id__in = players))


        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return self.update_funcs[request.query_params['action']](request, *args, **kwargs)
        
    # ---------- UPDATE sub-methods ---------- #
    def __apply__(self,  request, *args, **kwargs):
        params = request.query_params
        user = get_object_or_404(User, pk = params['user_id'])

        player, created = Player.objects.get_or_create(user = user, position = params['position'], name = user.name)
        if created:
            player.save()

        songplayer, created = SongPlayer.objects.get_or_create(player = player, song= self.get_object())
        if created:
            songplayer.save()

        
        instance = self.get_object()
        instance.players.add(songplayer)
        # save & forward 
        instance.save()
        serializer = SongSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def __quit__(self,  request, *args, **kwargs):
        params = request.query_params
        instance = self.get_object()

        user = get_object_or_404(User, pk = params['user_id'])
        player, created = Player.objects.get_or_create(user = user, position = params['position'])

        if created:
            # return 존재하지 않는 플레이어
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        songplayer, created = SongPlayer.objects.get_or_create(player = player, song = instance)
        if created:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        

        # player
        instance.players.remove(songplayer)
        instance.save()
        serializer = SongSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def __fix__(self,  request, *args, **kwargs):
        params = request.query_params
        selectedPlayers = json.loads(params['selectedPlayers'])

        
        positions = []
        players = []
        for pos, player in selectedPlayers.items():
            if player:
                # player가 있다면
                positions.append(pos)
                players.append(player)

        instance = self.get_object()

        # 곡에 포함된 전체 position
        # samePosition = instance.players.all().filter(
        #     Q(position__in = positions) 
        # )
        print(instance, selectedPlayers, players)

        allPlayers = instance.players.all()

        selected = allPlayers.filter(Q(id__in = players))
        notselected = allPlayers.exclude(Q(id__in = players))

        selected.update(fixed = True)
        notselected.update(fixed = False)
        print(allPlayers)
        print(selected)
        print(notselected)

        instance.save()
        serializer = SongSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
