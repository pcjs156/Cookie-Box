from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from django.utils import timezone

from .forms import LoginForm, UserSignUpForm, UserProfileForm
from .models import User, UserProfile

from Cookie_Box.settings import DEBUG


# 인증 코드 재발급을 요청하는 페이지
# 이미 이메일 인증이 완료된 경우 사용할 수 없음
# 마지막 인증 코드 재발급, 또는 회원가입으로부터 1시간이 지나야 다시 요청할 수 있음
def auth_code_reissue_view(request, username: str):
    content = dict()

    # 이미 해당 계정이 이메일 인증이 되어 있는 경우를 위한 플래그
    content['already_authenticated'] = False
    # 모든 조건이 성립해 인증 코드 재발급이 가능한 경우를 위한 플래그
    content['reissue_possible'] = True
    # 비밀번호가 틀렸을 경우를 위한 플래그
    content['wrong_password'] = False

    # 요청을 받은 경우
    if request.method == "POST":
        password = request.POST.get("password")

        user: User = authenticate(
            request=request,
            username=username,
            password=password,
        )

        # 로그인에 실패했을 경우
        if not user:
            content['wrong_password'] = True

        # 로그인에 성공한 경우
        # 입력된 인증 코드 재발급하고, 이메일을 전송한다.
        else:
            profile = UserProfile.get_profile_by_username(username)
            # 인증 코드를 갱신
            profile.set_auth_code()
            # 마지막으로 인증 코드 재발급 요청을 보낸 시간을 갱신
            profile.last_email_modified = timezone.now()
            profile.save()

            # 인증 코드 전송
            profile.send_auth_code()

            return redirect("unauthenticated", username)
    else:
        user: User = User.objects.get(username=username)
        profile: UserProfile = UserProfile.get_profile(user)

        # 이메일 인증을 이미 완료한 경우 인증 코드 재발급 할 수 없음
        if profile.email_authenticated:
            content['already_authenticated'] = True

        # 이메일 인증을 완료하지 않은 경우
        else:
            # 마지막 인증 코드 재발급 시각을 확인
            last_auth_code_request = profile.last_auth_code_request
            difference_sec = (timezone.localtime() -
                              last_auth_code_request).total_seconds()

            HOUR_SEC = 60**2
            # 디버깅모드인 경우 : 마지막 갱신시간으로부터 5초가 지났을 경우 가능
            if DEBUG is True:
                # 인증 코드 재발급이 불가능한 경우
                if difference_sec < 5:
                    content['reissue_possible'] = False
                    content['last_modifying'] = last_auth_code_request
                # 인증 코드 재발급이 가능한 경우
                else:
                    content['email'] = user.email
                    content['username'] = user.username
                    content['last_modifying'] = last_auth_code_request
            # 디버깅모드가 아닌 경우 : 마지막 인증 코드 재발급 시각과 현재 시각의 차이가 1시간 미만인 경우 가능
            else:
                # 인증 코드 재발급 불가능한 경우
                if difference_sec < HOUR_SEC:
                    content['reissue_possible'] = False
                    content['last_modifying'] = last_auth_code_request
                # 인증 코드 재발급이 가능한 경우
                else:
                    content['email'] = user.email
                    content['username'] = user.username
                    content['last_modifying'] = last_auth_code_request

    return render(request, 'auth_code_reissue.html', content)


# 이메일 주소 변경을 요청하는 페이지
# 이미 이메일 인증이 완료된 경우 사용할 수 없음
# 마지막 이메일 주소 변경, 또는 회원가입으로부터 1시간이 지나야 다시 요청할 수 있음
def email_modify_view(request, username: str):
    content = dict()

    # 이미 해당 계정이 이메일 인증이 되어 있는 경우를 위한 플래그
    content['already_authenticated'] = False
    # 모든 조건이 성립해 이메일 변경이 가능한 경우를 위한 플래그
    content['modifying_possible'] = True
    # 입력한 이메일이 이미 다른 유저가 사용중인 이메일인 경우를 위한 플래그
    content['already_used_email'] = False
    # 비밀번호가 틀렸을 경우를 위한 플래그
    content['wrong_password'] = False

    # 요청을 받은 경우
    if request.method == "POST":
        new_email = request.POST.get("new_email")
        password = request.POST.get("password")

        user: User = authenticate(
            request=request,
            username=username,
            password=password,
        )

        # 로그인에 실패했을 경우
        if not user:
            content['wrong_password'] = True

        # 자신이 이전에 사용하던 이메일을 포함해 이미 사용중인 이메일인 경우 변경 불가능
        all_users = User.objects.all()
        all_emails = list(user.email for user in all_users)
        if new_email in all_emails:
            content['already_used_email'] = True
            content['used_email'] = new_email

        # 로그인에 성공한 경우
        # 입력된 이메일로 변경하고, 이메일을 전송한다.
        else:
            profile = UserProfile.get_profile_by_username(username)
            # 인증 코드를 갱신
            profile.set_auth_code()
            # 마지막으로 이메일 변경 요청을 보낸 시간을 갱신
            profile.last_email_modified = timezone.now()
            profile.save()

            user = profile.user
            # 이메일을 갱신
            user.email = new_email
            profile.user.save()

            profile.send_auth_code()

            return redirect("unauthenticated", username)
    else:
        user: User = User.objects.get(username=username)
        profile: UserProfile = UserProfile.get_profile(user)

        # 이메일 인증을 이미 완료한 경우 이메일을 변경할 수 없음
        if profile.email_authenticated:
            content['already_authenticated'] = True

        # 이메일 인증을 완료하지 않은 경우
        else:
            # 마지막 이메일 변경 시각을 확인
            last_email_modifying = profile.last_email_modified
            difference_sec = (timezone.localtime() -
                              last_email_modifying).total_seconds()

            HOUR_SEC = 60**2
            # 디버깅모드인 경우 : 마지막 갱신시간으로부터 5초가 지났을 경우 가능
            if DEBUG is True:
                # 이메일 변경이 불가능한 경우
                if difference_sec < 5:
                    content['modifying_possible'] = False
                    content['last_modifying'] = last_email_modifying
                # 이메일 변경이 가능한 경우
                else:
                    content['email'] = user.email
                    content['username'] = user.username
                    content['last_modifying'] = last_email_modifying
            # 디버깅모드가 아닌 경우 : 마지막 이메일 변경 시각과 현재 시각의 차이가 1시간 미만인 경우 가능
            else:
                # 이메일 변경이 불가능한 경우
                if difference_sec < HOUR_SEC:
                    content['modifying_possible'] = False
                    content['last_modifying'] = last_email_modifying
                # 이메일 변경이 가능한 경우
                else:
                    content['email'] = user.email
                    content['username'] = user.username
                    content['last_modifying'] = last_email_modifying

    return render(request, 'email_modify.html', content)


# 로그인 페이지
# 만약 이메일 인증이 되지 않았을 경우 인증 페이지로 이동함
def logIn_view(request):
    content = dict()

    # ID/PW가 존재하지 않는 경우, 입력되지 않은 경우를 표시하기 위한 플래그
    content['wrong_information'] = False

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        content['form'] = form

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request=request,
                username=username,
                password=password,
            )

            # 인증이 완료된 경우 로그인 후 메인페이지로 이동
            if UserProfile.get_profile(user).email_authenticated:
                login(request, user)
                return redirect("main")
            # 인증이 되지 않은 경우 인증 페이지로 이동
            else:
                return redirect("unauthenticated", username)

        else:
            # ID/PW가 유효하지 않음을 표시
            content['wrong_information'] = True
            return render(request, 'logIn.html', content)

    else:
        form = LoginForm()
        content['form'] = form
        return render(request, 'logIn.html', content)


# 인증에 성공했을 때 보이는 페이지
def signUp_succeeded_view(request, username: str):
    content = dict()

    profile = UserProfile.get_profile_by_username(username)
    nickname = profile.nickname
    content['nickname'] = nickname

    return render(request, 'signUp_succeeded.html', content)


# 회원가입 뷰
# ID, 이메일, 닉네임 중복을 검증함
def signUp_view(request):
    content = dict()

    # 검증을 위해 불러옴
    all_users = User.objects.all()

    # 이미 존재하는 ID인 경우 False
    valid_username = True
    content['valid_username'] = valid_username
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
        user_signup_form = UserSignUpForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)

        if user_signup_form.is_valid() and user_profile_form.is_valid():
            # 이미 입력된 이메일인지 확인
            email = user_signup_form.cleaned_data.get("email")
            emails = list(user.email for user in all_users)
            valid_email = (email not in emails)
            content['valid_email'] = valid_email

            # 만약 이미 존재하는 이메일인 경우 다시 입력해야 함
            if not valid_email:
                content['user_signup_form'] = user_signup_form(request.POST)
                content['user_profile_form'] = user_profile_form(
                    request.POST, request.FILES)
                return render(request, 'signUp.html', content)

            # 이메일 검증을 통과했으면 안내 페이지로 이동
            else:
                user = user_signup_form.save()
                user.save()

                user_profile = user_profile_form.save(user, commit=False)
                user_profile.save()

                user_profile.send_auth_code()

                return redirect("unauthenticated", user.username)

        # 만약 유효하지 않은 form인 경우
        else:
            # 아래 ID/닉네임에서 유효성 검증을 해보고
            # 둘 다 유효한 경우 다른 요인에 의한 것임을 표시
            valid_form = True

            # 이미 존재하는 ID인지 확인
            username = user_signup_form.data.get("username")
            usernames = list(user.username for user in all_users)
            valid_username = (username not in usernames)
            content['valid_username'] = valid_username

            # 이미 사용중인 닉네임인지 확인
            nickname = user_profile_form.data.get("nickname")
            all_users_except_cur_user = User.objects.all().exclude(
                username=username)
            nicknames = [
                UserProfile.get_profile(user).nickname
                for user in all_users_except_cur_user
            ]
            valid_nickname = (nickname not in nicknames)
            content['valid_nickname'] = valid_nickname

            # ID/PW/닉네임 검증에서 막힌 것이면 예상치 못한 다른 문제로 인해 막힌 것이 아니므로
            if not (valid_username and valid_nickname):
                valid_form = True

            content['valid_form'] = valid_form

            content['user_signup_form'] = UserSignUpForm(request.POST)
            content['user_profile_form'] = UserProfileForm(
                request.POST,
                request.FILES,
            )
            return render(request, 'signUp.html', content)

    else:
        content['user_signup_form'] = UserSignUpForm()
        content['user_profile_form'] = UserProfileForm()
        return render(request, 'signUp.html', content)


@login_required(login_url='/account/logIn/')
# 로그아웃
def logOut(request):
    logout(request)
    return redirect("main")


# 이메일 인증 코드를 입력하는 페이지
# 회원가입 직후, 또는 이메일 인증이 되지 않은 상태에서 로그인을 시도할 때 뜸
def unauthenticated_view(request, username: str):
    content = dict()

    # 코드가 잘못 입력되었을 때 안내 문구를 표시하기 위한 플래그
    content['wrong_code'] = False

    user: User = User.objects.get(username=username)
    profile: UserProfile = UserProfile.get_profile(user)

    user_email = user.email
    content['user_email'] = user_email
    username = user.username
    content['username'] = username

    if request.method == "POST":
        # name이 auth_code인 input 태그의 값을 읽어옴
        auth_code = request.POST.get("auth_code").strip()
        # 발송된 인증 코드
        correct_code = profile.email_auth_code

        # 만약 인증 코드와 입력 코드가 같은 경우
        if correct_code == auth_code:
            # 이메일 인증에 완료한 것으로 표시하고 저장
            profile.email_authenticated = True
            profile.save()

            # 인증 완료 페이지로 이동
            return redirect("signUp_succeeded", user.username)

        # 인증 코드가 잘못 입력된 경우
        else:
            if auth_code is not None:
                # 플래그 설정
                content['wrong_code'] = True

            return render(request, 'unauthenticated.html', content)

    else:
        return render(request, 'unauthenticated.html', content)
