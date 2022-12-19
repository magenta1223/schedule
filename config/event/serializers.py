from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import
from project.serializers import SongSerializer
# from authentication.serializers import UserSerializer

class BaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseEvent
        fields = "__all__"

class PrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Private
        fields = "__all__"

class PulbicBlockSerializer(serializers.ModelSerializer):
    song = SongSerializer()
    class Meta:
        model = PulbicBlock
        fields = "__all__"

# auth views > aut 
class PublicSerializer(serializers.ModelSerializer):
    blocks = PulbicBlockSerializer(many = True)
    class Meta:
        model = Public
        fields = "__all__"