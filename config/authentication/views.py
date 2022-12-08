
from django.shortcuts import get_object_or_404
from rest_framework import viewsets # vieset import
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer # 생성한 serializer import
from .models import User # User model import
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import status, mixins, generics
from rest_framework import generics 

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })



class UserViewSet(viewsets.ModelViewSet): # ModelViewSet 활용
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, pk = None):
        kwargs = request.query_params
        user = get_object_or_404(User, pk = pk)
        user.name = kwargs['name']
        if kwargs['password']:
            user.password = kwargs['password']
        user.dateOfBirth = kwargs['dateOfBirth']
        user.save()

        return Response({}, status= status.HTTP_200_OK)




# 따로 만듭시다

@permission_classes([AllowAny]) #모든 사용자 접근가능
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # params = request.data

        # print("Create")
        # user = User(
        #     username = params['username'],
        #     password = params['password'],
        #     name = params['name'],
        # )
        # print("Done")

        # user.save()
        return Response({
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

@permission_classes([AllowAny]) #모든 사용자 접근가능
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):

        print(request.data)
        serializer = self.get_serializer(data=request.data)

        # LoginSerializer(context={'request': <rest_framework.request.Request: POST '/api/login/'>, 'format': None, 'view': <authentication.views.LoginView object>}, data={'username': 'admin@test.com', 'password': 'twhn1256'}):

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        print(serializer.validated_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_token = serializer.validated_data['access_token']
        refresh_token = serializer.validated_data['refresh_token']

        if user.id == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)
        
        

        response = {
            "user": UserSerializer(
                user,context=self.get_serializer_context()
                ).data, 
            "access_token": access_token,
            "refresh_token": refresh_token
            }
        
        print(response['user'])

        return Response(response) 