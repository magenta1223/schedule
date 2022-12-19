
from rest_framework import serializers # serializer import
from .models import User # 선언한 모델 import
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

# from event.serializers import BaseEventSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 20, write_only = True)
    # events = BaseEventSerializer(many = True)
    class Meta:
        model = User  # 모델 설정
        fields = '__all__'  # 필드 설정

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 20, write_only = True)

    class Meta:
        model = User
        fields = '__all__'  # 필드 설정

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            
            username = validated_data['username'],
            password = validated_data['password'],
            name = validated_data['name'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User  # 모델 설정
    
    username = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password", None)
        # 사용자 아이디와 비밀번호로 로그인 구현(<-> 사용자 아이디 대신 이메일로도 가능)
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return {'id': 'None','username':username}
        try:
            #payload = JWT_PAYLOAD_HANDLER(user) # payload 생성
            #jwt_token = JWT_ENCODE_HANDLER(payload) # jwt token 생성
            jwt_token = RefreshToken.for_user(user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )
        
        print(jwt_token)
        return {
            'user':user,
            'access_token': str(jwt_token.access_token),
            'refresh_token' : str(jwt_token)
        }