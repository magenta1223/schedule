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
    serializer_class = BaseEventSerializer
    queryset = BaseEvent.objects.all()
    permission_classes = [IsAuthenticated]
    userset = User.objects.all()

    def create(self, request, *args, **kwargs):
        params = request.query_params
        participants = [int(p) for p in json.loads(params['participants'])]
        user = get_object_or_404(User, pk = params['user_id'])
        participants = self.userset.filter(
            Q(id__in = participants)
        )
        print('event1!!!')
        event = BaseEvent(
            author = user,
            start = params['start'],
            end = params['end'],
            title = params['title'],
            content = params['content'],
            allDay = params['start'] == params['end']
        )
        event.save()
        event.participants.set(participants)
        event.save()
        event = BaseEventSerializer(event)
        return Response(event.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        params = request.query_params

        events = self.queryset.filter(
            Q(author__id = params['user_id']) | 
            Q(participants__in = params['user_id'])
        )

        serializer = self.get_serializer(data = events, many = True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        params = request.query_params

        event = get_object_or_404(BaseEvent, pk = params['event_id'])
        # 필요한 것은 song id, fixed여부. 일단 효율은 둘째치고 받았다. 

        event.start= params['start']
        event.end= params['end']
        event.title= params['title']
        event.content= params['content']
        event.save()

        serializer = self.get_serializer(event)

        return Response(serializer.data, status= status.HTTP_200_OK)   