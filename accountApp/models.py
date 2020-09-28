from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# 기본 Custom User Model / 일반 리뷰어
class CustomUser(AbstractUser, PermissionsMixin):
    class Meta:
        verbose_name = "유저"

    # 닉네임(또는 상호명)
    nickname = models.CharField(
        verbose_name="닉네임",
        max_length=15,
        blank=False,
        null=False,
        unique=True,
    )

    # 프로필 이미지
    # 빈 값으로 form에 입력될 경우 기본 이미지로 대체되어야 함
    image = models.ImageField(
        upload_to="accountApp/profile_image",
        default="accountApp/profile_image/user_default_image.png",
        blank=True,
        null=True,
        verbose_name="대표 이미지",
    )

    # 소개글
    introduce = models.TextField(
        verbose_name="소개글",
        default="",
        blank=True,
        null=False,
    )

    # 이메일 인증 여부
    email_authenticated = models.BooleanField(
        verbose_name="이메일 인증",
        default=False,
    )

    # 유저 레벨
    level = models.PositiveIntegerField(
        verbose_name="유저 레벨",
        default=1,
    )

    is_superuser = False