from django.urls import include, path
from rest_framework import routers, urls  # router import
from . import views  # views.py import

router = routers.DefaultRouter()  # DefaultRouter 설정
router.register('project', views.ProjectViewSet)  # ViewSet과 함께 user라는 router 등록
router.register('song', views.SongViewSet)  # ViewSet과 함께 user라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
]