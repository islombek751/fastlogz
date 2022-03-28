import os
from datetime import timedelta
from decouple import config
from pathlib import Path
SECRET_KEY = config('SECRET_KEY')
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ALLOWED_HOSTS = [
    '*'
]
GDAL_LIBRARY_PATH = ''
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-.023, 36.0),
    'DEFAULT_ZOOM': 5,
    'TILES': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
}
# Application definition
INSTALLED_APPS = [
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'django.contrib.gis',
    'leaflet',
    # apps
    'eld',
    'event',
    'log',
    # rest_framework
    'rest_framework',
    'rest_framework_gis',
    # simple_jwt blacklist
    'rest_framework_simplejwt.token_blacklist',
    # corsheaders
    'corsheaders',
    'baton.autodiscover',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors headers
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'system.wsgi.application'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
UPLOADED_FILES_USE_URL = True
# from rest_framework.permissions import DjangoModelPermissions
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'eld.perms.DisableRead',
        'rest_framework.permissions.IsAuthenticated'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,


    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=3),
}

# email sending settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fastlogzdev@gmail.com'
EMAIL_HOST_PASSWORD = 'wdcvdmbiyllyklxi'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# model abstract user
AUTH_USER_MODEL = 'eld.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


CORS_ORIGIN_ALLOW_ALL = True

BATON = {
    'SITE_HEADER': 'Fastlogs',
    'SITE_TITLE': 'fastlogs',
    'INDEX_TITLE': 'Fastlogs',
    'SUPPORT_HREF': 'https://t.me/shaxboz0201',
    'COPYRIGHT': '<a href=\'https://napaautomotive.uz/\'>copyright © Napa Automotive</a>', # noqa
    'POWERED_BY': '<a href=\'https://shaxbozaka.info\'>shaxbozaka</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': False,
    'GRAVATAR_DEFAULT_IMG': 'retro',
    'LOGIN_SPLASH': '/static/core/img/login-splash.png',
    'SEARCH_FIELD': {
        'label': 'Search contents...',
        'url': '/search/',
    },
    'MENU': (
        # {'type': 'title', 'label': 'Authentication', 'apps': ('eld', 'auth')},
        # {
        #     'type': 'free',
        #     'name': 'auth',
        #     'label': 'Groups',
        #     'icon': 'fa fa-lock',
        #     'url': '/admin/auth/group/',
        #     'models': (
        #         {
        #             'name': 'user',
        #             'label': 'Users'
        #         },
        #         {
        #             'name': 'group',
        #             'label': 'Groups'
        #         },
        #     )
        # },
        # {
        #     'type': 'free',
        #     'name': 'eld',
        #     'label': 'Users',
        #     'icon': 'fa fa-lock',
        #     'url': "/admin/eld/customuser/",
        #     'models': (
        #         {
        #             'name': 'customuser',
        #             'label': 'Users'
        #         },
        #         {
        #             'name': 'group',
        #             'label': 'Groups'
        #         },
        #     )
        # },

        {'type': 'free', 'icon': 'fa fa-lock', 'label': 'Authentication', 'default_open': True, 'children': [
            {'type': 'model', 'label': 'Users', 'name': 'customuser', 'app': 'eld'},
            {'type': 'model', 'label': 'Groups', 'name': 'group', 'app': 'auth'},
            {'type': 'model', 'label': 'Permissions', 'name': 'permission', 'app': 'auth'},
        ]},
        {
            'type': 'app',
            'default_open': True,
            'name': 'eld',
            'label': 'ELD',
            'icon': 'fa',
            'url': '/admin/auth/group/',
            'models': (
                {
                    'name': 'company',
                    'label': 'Companies'
                },
                {
                    'name': 'eld',
                    'label': 'ELD\'s'
                },
                {
                    'name': 'vehicle',
                    'label': 'Vehicles'
                },
                {
                    'name': 'drivers',
                    'label': 'DRIVERS'
                },
            )
        },

    ),
    # 'ANALYTICS': {
    #     'CREDENTIALS': os.path.join(BASE_DIR, 'credentials.json'),
    #     'VIEW_ID': '12345678',
    # }
}

redis_host = os.environ.get('REDIS_HOST', 'localhost')


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# CACHE_TTL = 60 * 1
