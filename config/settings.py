from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

environ.Env.read_env(env.str("DOTENV_PATH", ".env"))

VERSION = env("VERSION", default="1")
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    # UNFOLD
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    # DJANGO
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # APPS
    "etc.apps.EtcConfig",
    "account.apps.AccountConfig",
    "chat.apps.ChatConfig",
    "game.apps.GameConfig",
    "notification.apps.NotificationConfig",
    # EXTRA
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "channels",
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
]

ROOT_URLCONF = "config.urls"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "account.bl.auth.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Volley Pro API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [
        {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    ],
    "SECURITY_DEFAULT": [{"Bearer": []}],
}

JWT_ACCESS_TOKEN_LIFETIME = timedelta(hours=env.float("ACCESS_TOKEN_LIFETIME", 1))
JWT_REFRESH_TOKEN_LIFETIME = timedelta(hours=env.float("REFRESH_TOKEN_LIFETIME", 168))
JWT_SIGNING_KEY = env.str("SIGNING_KEY", "test")
JWT_ALGORITHM = "HS256"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": env.str("DB_ENGINE", "django.db.backends.postgresql"),
#         "NAME": env.str("DB_NAME", "volley_pro"),
#         "USER": env.str("DB_USER", "postgres"),
#         "PASSWORD": env.str("DB_PASSWORD", "postgres"),
#         "HOST": env.str("DB_HOST", "localhost"),
#         "PORT": env.str("DB_PORT", "5432"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "volley_pro",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# REDIS
REDIS_HOST = env.str("REDIS_HOST", "localhost")
REDIS_PORT = env.str("REDIS_PORT", "6379")
REDIS_URL = env.str("REDIS_URL", default=f"redis://{REDIS_HOST}:{REDIS_PORT}")

# CELERY
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default=f"{REDIS_URL}/0")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default=f"{REDIS_URL}/0")

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465

EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# CLICKHOUSE
CLICKHOUSE_HOST = env.str("CLICKHOUSE_HOST", default="localhost")
CLICKHOUSE_PORT = env.str("CLICKHOUSE_PORT", default="8123")
CLICKHOUSE_DATABASE = env.str("CLICKHOUSE_DATABASE", default="volley_pro")
CLICKHOUSE_USER = env.str("CLICKHOUSE_USER", default="default")
CLICKHOUSE_PASSWORD = env.str("CLICKHOUSE_PASSWORD")

AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8000",
    ],
)


# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": env.str("REDIS_URL", default="redis://localhost:6379/1"),
#     }
# }


UNFOLD = {
    "SITE_TITLE": "Volley Pro Admin",
    "SITE_HEADER": "Volley Pro",
    "SITE_SYMBOL": "sports_volleyball",
}
