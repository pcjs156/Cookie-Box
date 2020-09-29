from django.db import models
from django.contrib.auth.models import User

# 인증 코드 생성
import random
from string import ascii_uppercase, digits

# 인증 코드에 사용될 문자 : 알파벳 대문자 + 숫자
CODE_CHARACTERS = ascii_uppercase + digits
# 인증 코드의 길이
AUTH_CODE_LEN = 8

# 이메일 전송
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class UserProfile(models.Model):
    class Meta:
        verbose_name = "유저 정보"

    def __str__(self):
        return f"Profile of [{self.user}]"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="대상 유저",
        related_name="user_profile",
    )

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
        verbose_name="이메일 인증 여부",
        default=False,
    )

    # 이메일 인증 코드 : 8자리
    email_auth_code = models.CharField(
        verbose_name="이메일 인증 코드",
        default="",
        max_length=AUTH_CODE_LEN,
    )

    # 마지막으로 인증 코드를 재발급 요청한 때
    last_auth_code_request = models.DateTimeField(
        verbose_name="마지막 인증 코드 요청",
        auto_now_add=True,
    )

    # 인증 코드를 생성하는 메서드
    # 알파벳 대문자 + 숫자 조합의 8자리 코드가 생성됨
    def get_auth_code(self):
        return ''.join(
            random.choice(CODE_CHARACTERS) for _ in range(AUTH_CODE_LEN))

    # 인증 코드를 초기화하는 메서드
    def set_auth_code(self):
        self.email_auth_code = self.get_auth_code()

    def send_auth_code(self):
        # 인증 코드를 담은 html 메일 템플릿을 생성
        message = render_to_string('authenticate_mail.html', {
            'code': self.email_auth_code,
        })

        # 이메일 전송 설정
        mail_subject = "Cookie Box 회원가입 인증 메일입니다."
        # 이메일을 보낼 대상 설정
        user_email = self.user.email
        # 주의! to=[] 안에 들어가는 이메일 주소로 해당 이메일을 수신받으면
        # to 안에 있는 모든 유저가 자기 외에 해당 이메일을 발급받은 모든 이메일 주소를
        # 확인할 수 있으므로 for문으로 한 명씩 처리해야 함
        email = EmailMessage(mail_subject, message, to=[self.user.email])
        # 이메일 전송
        email.send()

    # 마지막으로 이메일 수정 요청을 한 때
    last_email_modified = models.DateTimeField(
        verbose_name="마지막 이메일 재설정",
        auto_now_add=True,
    )

    # 유저 레벨
    level = models.PositiveIntegerField(
        verbose_name="유저 레벨",
        default=1,
    )

    # 이하 get_profile ==========================
    # 공통적으로 검색에 실패하면 None 반환====

    # User 모델의 username으로 특정 유저를 검색
    @staticmethod
    def get_profile_by_username(username: str):
        user = User.objects.get(username=username)
        return UserProfile.objects.get(user=user)

    # User 모델을 입력 받아 바로 검색
    @staticmethod
    def get_profile(user: User):
        return UserProfile.objects.get(user=user)

    # 이상 get_user ==========================
