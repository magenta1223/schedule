from django.db import models

# Create your models here.
from django.utils import timezone

from authentication.models import User

class BaseEvent(models.Model):
    """
    Base class for various events
    """

    author = models.ForeignKey(User, verbose_name= '작성자',on_delete=models.CASCADE, null=True, related_name= 'events')
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    
    start = models.DateTimeField(verbose_name = "start")
    end = models.DateTimeField(verbose_name = "end")

    title = models.CharField(verbose_name = "name",  max_length=20)
    content = models.TextField(verbose_name = "desc")
    
    participants = models.ManyToManyField(User, related_name= "참여인원")

    allDay = models.BooleanField(default= False)

    STATUS_CHOICES = (
        ('P', 'Private'),
        ('S', 'Shared'),
        ('O', 'OnGoing'),
        ('D', 'Done'),
    )
    cls = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")

    class Meta:
        verbose_name_plural = "이벤트"
        verbose_name = "이벤트"