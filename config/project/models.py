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
    
    # 세션 채워야됨. 
    # user와 many-to-many
    # 필요한 세션이 막 ㅈㄴ 많을 수도 있음.
    # session model을 만들어서 마구 추가할 수 있어야 함.
    # song에서 필요한 session만 체크하면 됨. 1대 다? 
    # 기타 추가 > G1, G2, G3 .. 
    # 그리고 각각에 사람을 매핑시켜야 됨. 

    # inst는 종류가 여러개, 각 종류 별로 여러개 필요.
    # 필요에 따라서는 특수악기를 넣어야 함
    
    # 조건 체크
    # 필요 악기가 모두 채워졌는지?
    # 일단 session은 모델로 만들면 안됨. 가변길이를 가짐. 
    # session은 json field로 만들고, 생성 시 기본값은 False나 None으로 줌.
    # 그리고 줄서기를 하면 거기에 user들이 추가되고
    # select 시 값이 한명이 됨.
    # 최소 1명 이상이 있으면 조건 충족. 
    
    instruments = models.JSONField(verbose_name= "positions", default= [])
    # dictionary일 필요가 전혀 없음. 그냥 list로도 충분함. 
    # project.Song.instruments: (fields.E010) JSONField default should be a callable instead of an instance so that it's not shared between all field instances.
    # HINT: Use a callable instead, e.g., use `dict` instead of `{}`.

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
    fixed = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.song.title} {self.player.position.upper()} {self.player.user.name} {self.id}"

    class Meta:
        # 복수형 저장. 관리자페이지에서 이 이름으로 보인다
        verbose_name = '곡에 bind된 연주자'
        verbose_name_plural = '곡에 bind된 연주자'    