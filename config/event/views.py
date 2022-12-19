from django.shortcuts import render
# django rest framework
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response

# django
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

# core apps
from .serializers import * 
from .models import * 

# auth
from authentication.models import User

import json

class BaseEventViewSet(viewsets.ModelViewSet):
    """
    Create, List, Delete는 여기서
    Retrieval / Update는 따로 
    """
    serializer_class = BaseEventSerializer
    queryset = BaseEvent.objects.all()
    permission_classes = [IsAuthenticated]
    userset = User.objects.all()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.list_funcs = {
            'base' : self.__list_base__,
            'private' : self.__list_private__,
            'public' : self.__list_public__,
        }
    
    def list(self, request, *args, **kwargs):

        print(request.query_params)

        return self.list_funcs[request.query_params['type']](request, *args, **kwargs)

    # list funcs
    def __list_base__(self, request, *args, **kwargs):
        params = request.query_params
        events = self.queryset.filter(
            Q(author__id = params['user_id']) | 
            Q(participants__in = params['user_id'])
        )
        serializer = self.get_serializer(data = events, many = True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


    def __list_private__(self, request, *args, **kwargs):
        params = request.query_params
        events = Private.objects.all().filter(
            Q(author__id = params['user_id']) | 
            Q(participants__in = params['user_id'])
        )
        serializer = self.get_serializer(data = events, many = True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def __list_public__(self, request, *args, **kwargs):
        params = request.query_params
        # project = get_object_or_404(Project, pk = params['project_id'])

        # meetings = project.meetings
        # get_list_or_404(Public, )
        meetings = Public.objects.filter(
            Q(project__id = params['project_id'])
        )
        serializer = PublicSerializer(data = meetings, many = True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)



    def update(self, request, *args, **kwargs):
        params = request.query_params

        event = get_object_or_404(BaseEvent, pk = params['event_id'])
        # 필요한 것은 song id, fixed여부. 일단 효율은 둘째치고 받았다.
        # 여기서는 각 event viewset의 update method를 전부 따로 구현.  

        event.start= params['start']
        event.end= params['end']
        event.title= params['title']
        event.content= params['content']
        event.save()

        serializer = self.get_serializer(event)

        return Response(serializer.data, status= status.HTTP_200_OK)   



class PrivateViewset(viewsets.ModelViewSet):
    serializer_class = PrivateSerializer
    queryset = Private.objects.all()
    permission_classes = [IsAuthenticated]
    userset = User.objects.all()

    def create(self, request, *args, **kwargs):
        params = request.query_params
        participants = [int(p) for p in json.loads(params['participants'])]
        user = get_object_or_404(User, pk = params['user_id'])
        participants = self.userset.filter(
            Q(id__in = participants)
        )
        event = Private(
            author = user,
            start = params['start'],
            end = params['end'],
            title = params['title'],
            content = params['content'],
            allDay = params['start'] == params['end'],
            cls = "private"
        )
        event.save()
        event.participants.set(participants)
        event.save()
        event = PrivateSerializer(event)
        return Response(event.data, status=status.HTTP_200_OK)
    
    

class PublicViewset(viewsets.ModelViewSet):
    serializer_class = PublicSerializer
    queryset = Public.objects.all()
    permission_classes = [IsAuthenticated]
    userset = User.objects.all()

    def create(self, request, *args, **kwargs):
        params = request.query_params


        meeting = json.loads(params['meeting'])
        project = get_object_or_404(Project, pk = params['project_id'])
        author = get_object_or_404(User, pk = params['user_id'])
        
        print(meeting['schedules'])
        # schedules = [ { k : (v if k !="song" else v['id']) for k, v in s.items()}   for s in meeting['schedules']]
        


        # 필수 참가자를 브라우저에서 계산하게 하자

        participants = self.userset.filter(
            Q(id__in = meeting['participants'])
        )

        public = Public(
            author = author,
            start = meeting['start'], 
            end = meeting['end'],
            title = meeting['title'],
            content = meeting['content'],
            project = project,
            cls = "public"
        )

        public.save()
        public.participants.set(participants)
        for schedule in meeting['schedules']:
            song = get_object_or_404(Song, pk = schedule['song']['id'])
            pb = PulbicBlock(
                author = author,
                start = schedule['start'], 
                end = schedule['end'],
                title = song.title,
                cls = "pBlock",
                song = song
            )
            pb.save()
            public.blocks.add(pb)

        public.save()
        public = PublicSerializer(public)

        return Response(None, status=status.HTTP_200_OK)


