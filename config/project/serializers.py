from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import

from authentication.serializers import UserSerializer
# from event.serializers import PublicSerializer

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = "__all__"

class SongPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    class Meta:
        model = SongPlayer
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    players = SongPlayerSerializer(many = True)
    class Meta:
        model = Song
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # 목적별로 serializer 분류해서 최적화
    songs = SongSerializer(many=True)
    # meetings = PublicSerializer(many = True)
    class Meta:
        model = Project
        fields = '__all__'

