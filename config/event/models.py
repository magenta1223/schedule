from django.db import models

# Create your models here.
from django.utils import timezone

from authentication.models import User
from project.models import Project, Song

class BaseEvent(models.Model):
    """
    Base class for various events
    """

    author = models.ForeignKey(User, verbose_name= '작성자',on_delete=models.CASCADE, null=True, related_name= 'events')
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    
    start = models.DateTimeField(verbose_name = "start")
    end = models.DateTimeField(verbose_name = "end")

    title = models.CharField(verbose_name = "name",  max_length=20)
    # content = models.TextField(verbose_name = "desc")
    participants = models.ManyToManyField(User, related_name= "참여인원")
    allDay = models.BooleanField(default= False)
    
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('pBlock', 'PublicBlock'),
    )
    cls = models.CharField(max_length=10, choices=STATUS_CHOICES, default="private")

    class Meta:
        verbose_name_plural = "이벤트"
        verbose_name = "이벤트"



class Private(BaseEvent):
    content = models.TextField(verbose_name = "desc", default= "")
    class Meta:
        verbose_name_plural = "개인 스케쥴"
        verbose_name = "개인 스케쥴"

class PulbicBlock(BaseEvent):
    # song
    song = models.ForeignKey(Song, on_delete= models.CASCADE, related_name= "meetings")
    class Meta:
        verbose_name_plural = "블록"
        verbose_name = "블록"

class Public(BaseEvent):
    """
    High Level Wrapper class for meeting. 
    """
    content = models.TextField(verbose_name = "desc", default= "")
    project = models.ForeignKey(Project, on_delete= models.CASCADE, related_name= "meetings")
    # schedules = models.JSONField(verbose_name= "schedules", default= [])
    blocks = models.ManyToManyField(PulbicBlock, related_name="cex")

    class Meta:
        verbose_name_plural = "프로젝트 미팅"
        verbose_name = "프로젝트 미팅"