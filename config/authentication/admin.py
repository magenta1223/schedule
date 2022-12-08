# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# from .forms import UserCreateForm, UserChangeForm

# # Register your models here.
# class UserAdmin(UserAdmin):
#     """사용자 인스턴스를 추가하고 변경하는 양식"""
#     form = UserChangeForm
#     add_form = UserCreateForm

#     list_display = ('username',)
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('username', 'age', 'city')}),
#     )

# admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreateForm, UserChangeForm

from .models import User

class UserAdmin(UserAdmin):
    model = User
    # 유저 목록
    list_display = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )
    
admin.site.register(User, UserAdmin)