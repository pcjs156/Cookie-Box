from django import forms
from django.contrib.auth.forms import AuthenticationForm

# 비밀번호 hashing
from django.db import transaction
from django.contrib.auth.hashers import make_password

from .models import User, UserProfile


# 로그인 폼
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# 아이디, 비밀번호, 이메일 폼
class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    # 평문으로 입력된 비밀번호를 hashing해서 저장
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        user.password = make_password(user.password)
        return user


# 닉네임, 자기소개, 대표 이미지 폼
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'introduce', 'image']

    # save 메서드 호출시 자동으로 인증 코드 생성
    @transaction.atomic
    def save(self, user, commit=True):
        profile = super().save(commit=commit)
        profile.user = user
        profile.set_auth_code()
        profile.save()
        return profile
