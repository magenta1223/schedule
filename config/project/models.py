from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone

from authentication.models import User


class Project(models.Model):
    """
    Project
    """
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)
    title = models.CharField(verbose_name= '이름', max_length=20, unique=True)
    content = models.TextField(verbose_name='내용')

    STATUS_CHOICES = (
        ('P', 'Prepare'),
        ('R', 'Ready'),
        ('O', 'OnGoing'),
        ('D', 'Done'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '프로젝트'
        verbose_name = '프로젝트'

class Player(models.Model):
    """
    Player
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    position = models.CharField(max_length= 20)
    name = models.CharField(max_length= 20, default= "unnamed")
    # fixed = models.BooleanField(default= False)
    # name = models.CharField(max_length= 20)

    def __str__(self):
        return f"{self.position.upper()} {self.user.name}"

    class Meta:
        verbose_name_plural = '연주자'
        verbose_name = '연주자'

    
class Song(models.Model):
    """
    Song for the project
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자', auto_now= True)
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)
    title = models.CharField(verbose_name= '곡명', max_length=50)
    artist = models.CharField(verbose_name= '아티스트', max_length=50)
    content = models.TextField(verbose_name='비고')
    
    instruments = models.JSONField(verbose_name= "positions", default= [])

    project = models.ForeignKey(Project, verbose_name= '프로젝트', related_name='songs', on_delete=models.CASCADE, null = True, blank = True)
    #notice = models.BooleanField(verbose_name= "상단고정게시물", null=True, blank=True)

    fix = models.BooleanField(default = False)

    def __str__(self):
        return self.title
    

    @property
    def complete(self):
        for k, v in self.instruments.items():
            if not len(v):
                return False
        return True

    class Meta:
        # 복수형 저장. 관리자페이지에서 이 이름으로 보인다
        verbose_name = '곡'
        verbose_name_plural = '곡'

class SongPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete= models.CASCADE)
    song = models.ForeignKey(Song, on_delete= models.CASCADE, related_name= 'players')
    fixed = models.BooleanField(default= False) # 이 추가 field 때문에 반드시 이렇게 사용해야 함. 

    def __str__(self):
        return f"{self.song.title} {self.player.position.upper()} {self.player.user.name} {self.id}"

    class Meta:
        # 복수형 저장. 관리자페이지에서 이 이름으로 보인다
        # fixed라
        verbose_name = '곡에 bind된 연주자'
        verbose_name_plural = '곡에 bind된 연주자'    