from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

from .forms import LoginForm, SignUpForm
from .models import CustomUser

from .tokens import account_activation_token


def signUp_succeeded_view(request, username: str):
    content = dict()

    user: CustomUser = CustomUser.objects.get(username=username)
    user_email = user.email
    content['user_email'] = user_email

    return render(request, 'signUp_succeeded.html', content)


def unauthenticated_view(request, username: str):
    content = dict()

    user: CustomUser = CustomUser.objects.get(username=username)
    user_email = user.email
    content['user_email'] = user_email

    return render(request, 'unauthenticated.html', content)


def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = CustomUser.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.email_authenticated = True
        user.save()
        login(request, user)
        return redirect('main')
    else:
        return HttpResponse('비정상적인 접근입니다.')


# 회원가입 뷰
def signUp_view(request):
    content = dict()

    # 검증을 위해 불러옴
    all_users = CustomUser.objects.all()

    # 이미 존재하는 ID인 경우 False
    valid_username = True
    content['valid_username'] = valid_username
    # 입력된 비밀번호/비밀번호 확인이 다른 경우 False
    valid_pw = True
    content['valid_pw'] = valid_pw
    # 이미 입력된 이메일인 경우 False
    valid_email = True
    content['valid_email'] = valid_email
    # 이미 사용중인 닉네임인 경우 False
    valid_nickname = True
    content['valid_nickname'] = valid_nickname

    # 정의하지 않은 기타 오류
    valid_form = False
    content['valid_form'] = valid_form

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            # 이미 입력된 이메일인지 확인
            email = form.cleaned_data.get("email")
            emails = list(user.email for user in all_users)
            valid_email = (email not in emails)
            content['valid_email'] = valid_email

            # 만약 이미 존재하는 이메일인 경우 다시 입력해야 함
            if not valid_email:
                content['form'] = SignUpForm(request.POST, request.FILES)
                return render(request, 'signUp.html', content)

            # 이메일 검증을 통과했으면 안내 페이지로 이동
            else:
                user = form.save()
                user.save()

                current_site = get_current_site(request)
                # 127.0.0.1:8000
                message = render_to_string(
                    'authenticate_mail.html', {
                        'user':
                        user,
                        'domain':
                        current_site.domain,
                        'uid':
                        urlsafe_base64_encode(force_bytes(
                            user.pk)).encode().decode(),
                        'token':
                        account_activation_token.make_token(user),
                    })

                mail_subject = "Cookie Box 회원가입 인증 메일입니다."
                user_email = user.email
                email = EmailMessage(mail_subject, message, to=[user_email])
                email.send()

                return signUp_succeeded_view(request, user.username)

        else:
            valid_form = True

            # 이미 존재하는 ID인지 확인
            username = form.data.get("username")
            usernames = list(user.username for user in all_users)
            valid_username = (username not in usernames)
            content['valid_username'] = valid_username

            # 비밀번호/비밀번호 확인이 같은지 확인
            pw1 = form.data.get("password1")
            pw2 = form.data.get("password2")
            valid_pw = (pw1 == pw2)
            content['valid_pw'] = valid_pw

            # 이미 사용중인 닉네임인지 확인
            nickname = form.data.get("nickname")
            nicknames = list(user.nickname for user in all_users)
            valid_nickname = (nickname not in nicknames)
            content['valid_nickname'] = valid_nickname

            # ID/PW/닉네임 검증에서 막힌 것이면 정의되지 않은 다른 문제로 인해 막힌 것이 아니므로
            if not (valid_username and valid_pw and valid_nickname):
                valid_form = True

            content['valid_form'] = valid_form

            content['form'] = SignUpForm(request.POST, request.FILES)
            return render(request, 'signUp.html', content)

    else:
        content['form'] = SignUpForm()
        return render(request, 'signUp.html', content)


# 로그인 페이지
def logIn_view(request):
    content = dict()

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        content['form'] = form

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request=request,
                                username=username,
                                password=password)

            # 인증이 완료된 경우 로그인 후 메인페이지로 이동
            if user.email_authenticated:
                login(request, user)
                return redirect("main")
            # 인증이 되지 않은 경우 인증 요구 페이지로 이동
            else:
                return unauthenticated_view(request, username)

        else:
            return render(request, 'logIn.html', content)

    else:
        form = LoginForm()
        content['form'] = form
        return render(request, 'logIn.html', content)


@login_required(login_url='/account/logIn/')
# 로그아웃
def logOut(request):
    logout(request)
    return redirect("main")