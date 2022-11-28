"""Django settings for apex project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import environ
from corsheaders.defaults import default_headers, default_methods
from firebase_admin import initialize_app

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# django environ configuration starts here
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGIN_REGEXES=(list, []),
)

environ.Env.read_env()
# django environ configuration ends here

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-(nv23-80)topw_k1uw(8ib=5%+jrida67biofm(f3vvli6o1y^",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    # channels is placed at top as recommneded in its docs
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # custom models
    "accounts",
    "common",
    "notes",
    "courses",
    "exams",
    "enrollments",
    "attendance",
    "clock",
    "physicalbook",
    "payments",
    "meetings",
    "infocenter",
    # third party
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "django_filters",
    "nested_admin",
    "django_celery_results",
    "django_celery_beat",
    "ckeditor",
    "debug_toolbar",
    "fcm_django",
    "notifications",
    "report",
    "bannerad",
    "counseling",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apex.middleware.MoveJWTCookieIntoTheBody",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "apex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apex.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

password_validator = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{password_validator}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{password_validator}.MinimumLengthValidator",
    },
    {
        "NAME": f"{password_validator}.CommonPasswordValidator",
    },
    {
        "NAME": f"{password_validator}.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = env("STATIC_URL")
if DEBUG:
    STATICFILES_DIRS = [(BASE_DIR / "static")]
else:
    STATICFILES_ROOT = [(BASE_DIR / "static")]
STATIC_ROOT = BASE_DIR / "static-live"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth User Start
AUTH_USER_MODEL = "accounts.User"
# Auth User End

# Rest Framework Start
REST_FRAMEWORK = {
    # "DEFAULT_PAGINATION_CLASS": "courses.api.paginations.CustomPagination",
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
# Rest Framework End

# OTP Start
OTP_SEND_URL = env("OTP_SEND_URL", default="https://sms.aakashsms.com/sms/v3/send")
OTP_SMS_TOKEN = env("OTP_SMS_TOKEN", default="aakash")
OTP_SMS_PLATFORM = env("OTP_SMS_PLATFORM", default="AakashSMS")
OTP_EXPIRY_SECONDS = env("OTP_EXPIRY_SECONDS", default=120)
OTP_SMS_FROM = env("OTP_SMS_FROM", default="Apex")
# OTP End

# JWT dj-rest-auth Start
REST_USE_JWT = True
JWT_AUTH_COOKIE = env("JWT_AUTH_COOKIE", default="jwt_auth")
JWT_AUTH_REFRESH_COOKIE = env("JWT_AUTH_REFRESH_COOKIE", default="jwt_refresh")
JWT_AUTH_SAMESITE = env("JWT_AUTH_SAMESITE", default="none")
JWT_AUTH_SECURE = env("JWT_AUTH_SECURE", default=False)
JWT_AUTH_RETURN_EXPIRATION = True
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.api.serializers.UserCustomDetailsSerializer",
}
# JWT dj-rest-auth End

# Cors

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = list(default_methods) + []
CORS_ALLOW_HEADERS = list(default_headers) + [
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Credentials",
    "responseType",
]


CORS_ALLOWED_ORIGIN_REGEXES = env(
    "CORS_ALLOWED_ORIGIN_REGEXES",
    default=[
        r"^http://localhost:\d+",
        r"^http://192.168.\d+.\d+:\d+",
        r"^http://.*.ngrok.io",
    ],
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:3001",
    ],
)
# cors end

# simple jwt config start
USER_AUTHENTICATION_RULE = (
    "rest_framework_simplejwt.authentication.default_user_authentication_rule"
)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("ACCESS_EXPIRY_TIME", default=5)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=env.int("REFRESH_EXPIRY_TIME", default=1440)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": USER_AUTHENTICATION_RULE,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
# simple jwt config end

APPEND_SLASH = True

# So that if error while saving then the save process will roll back
ATOMIC_REQUESTS = True

# so that while entering exam max post fields exceeded error will not be raised
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Celery settings
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="django-db")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"
# celery settings end

# ckeditor settings start
CKEDITOR_BASEPATH = f"/{STATIC_URL}ckeditor/ckeditor/"

# CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"
CKEDITOR_MATHJAX_URL = (
    "//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML"
)
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono-lisa",
        # 'skin': 'office2013',
        "toolbar_Custom": [
            {"name": "formats", "items": ["Bold", "Italic", "Underline"]},
            {
                "name": "math",
                "items": [
                    "Mathjax",
                ],
            },
            {
                "name": "source",
                "items": ["Source", "Preview"],
            },
        ],
        "toolbar": "Custom",
        "mathJaxLib": CKEDITOR_MATHJAX_URL,
        "height": 200,
        "width": 600,
        "extraPlugins": ",".join(
            [
                "mathjax",
            ]
        ),
        "pasteFromWordRemoveFontStyles": True,
        "pasteFromWordPromptCleanup": True,
        "forcePasteAsPlainText": True,
        "ignoreEmptyParagraph": True,
    },
}
# ckeditor settings end

# Email settings start
EMAIL_CONFIG = env.email_url(
    "EMAIL_URL", default="consolemail://test@example.com:password@localhost:25"
)
vars().update(EMAIL_CONFIG)
# Email settings end

# server Bug tracker settings start
SERVER_EMAIL = EMAIL_CONFIG["EMAIL_HOST_USER"]
ADMINS = [
    ("Apex Error", "sushilk.calcgen@gmail.com"),
    ("Apex Error", "raj.shrestha778@gmail.com"),
]
# server Bug tracker settings end

# For providing https route start
HTTPS_ENABLED = env("HTTPS_ENABLED", default=False)

if HTTPS_ENABLED:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# For providing https route end

# Channels settings start
ASGI_APPLICATION = "apex.asgi.application"

redis_url = env("REDIS_URL", default="redis://localhost:6379")
redis_host = env("REDIS_HOST", default="localhost")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
            # "hosts": [("127.0.0.1", 6379)],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{redis_url}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Cache time to live is 2 days
CACHE_TTL = 60 * 60 * 24 * 2

INTERNAL_IPS = [
    "127.0.0.1",
]

ZOOM_CONFIGS = {
    "zoom_key": env("ZOOM_KEY"),
    "zoom_account_id": env("ZOOM_ACCOUNT_ID"),
    "zoom_api": env("ZOOM_API_URL", default="https://api.zoom.us/v2/"),
    "zoom_retry_attempts": env("ZOOM_RETRY_ATTEMPTS", default=3),
    "zoom_sdk_key": env("ZOOM_SDK_KEY"),
    "zoom_secret_key": env("ZOOM_SECRET_KEY"),
}
# firebase notification
FIREBASE_APP = initialize_app()
FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "Apex",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}
GOOGLE_APPLICATION_CREDENTIALS = BASE_DIR / env(
    "GOOGLE_APPLICATION_CREDENTIALS", default="apex-education-firebase.json"
)
# Firebase notification end
