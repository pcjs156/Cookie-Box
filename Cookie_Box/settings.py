import os, json

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secretKey.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)


SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = "accountApp.CustomUser"

# Application definition

# 직접 작성하지 않은 앱
THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'six',
    'django_inlinecss',
]

# 직접 작성한 앱
SERVICE_APPS = [
    'mainApp',
    'accountApp',
    'blogApp',
    'mailingApp',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + SERVICE_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Cookie_Box.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Cookie_Box.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEditor 관련 =============================================

# CKEDitor 이미지 업로드 위치
CKEDITOR_UPLOAD_PATH = 'editor_uploads/'

# 이미지 썸네일을 처리하는 라이브러리? 지정?
CKEDITOR_IMAGE_BACKEND = "pillow"

# 이미지 썸네일 크기 조정
# CKEDITOR_THUMBNAIL_SIZE = (75, 75) -> 기본값

# 자기가 올린 이미지만 열람할 수 있도록 제한
CKEDITOR_RESTRICT_BY_USER = True

# 아마도 올린 파일을 year/month/day 단위로 확인할 수 있는 기능인듯
CKEDITOR_RESTRICT_BY_DATE = True

# 이미지가 아닌 파일을 업로드 할 수 없도록 제한
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# 이미지가 제대로 보이지 않으면 아래 주석 해제
# X_FRAME_OPTIONS = 'SAMEORIGIN'

# E-mailing 관련 ============================================
email_info = os.path.join(BASE_DIR, 'email_info.json')

with open(email_info) as f:
    email_info = json.loads(f.read())


def get_email_info(setting, email_info=email_info):
    try:
        return email_info[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)


EMAIL_HOST = get_email_info("EMAIL_HOST")
EMAIL_PORT = int(get_email_info("EMAIL_PORT"))
EMAIL_HOST_USER = get_email_info("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_email_info("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
