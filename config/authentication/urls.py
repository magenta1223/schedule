
from django.urls import include, path
from rest_framework import routers, urls  # router import
from . import views  # views.py import

router = routers.DefaultRouter()  # DefaultRouter 설정
router.register('user', views.UserViewSet)  # ViewSet과 함께 user라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
]