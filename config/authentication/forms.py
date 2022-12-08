
from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import models

class UserCreateForm(forms.ModelForm):
    """
    form for creating user
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)  # "__all__"

    def clean_password2(self):
        """
        두 암호가 일치하는지 확인
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
              raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        제공된 비밀번호를 해시 형식으로 저장
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
              user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    Form for updating user
    """
    password = ReadOnlyPasswordHashField()
    username = models.CharField(verbose_name='이름', max_length= 20)

    class Meta:
        model = User
        fields = ('username', 'password', 'is_active')
