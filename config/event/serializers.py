from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import

# from authentication.serializers import UserSerializer

class BaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseEvent
        fields = "__all__"