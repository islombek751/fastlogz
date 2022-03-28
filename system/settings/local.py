from .base import *
import environ

env = environ.Env(DEBUG=(bool,False))
environ.Env.read_env(env_file=".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")
DEBUG = config('DEBUG')

# DATABASES = {
# 'default': {
#     'ENGINE': 'django.contrib.gis.db.backends.postgis',
#     'NAME': env("POSTGRES_DBNAME"),                      
#     'USER':  env("POSTGRES_USER"),
#     'PASSWORD':  env("POSTGRES_PASS"),
#     'HOST': env("PG_HOST"),
#     'PORT':  env("PG_PORT"),
#     }
# }


redis_host = os.environ.get('REDIS_HOST', 'localhost')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# GDAL_LIBRARY_PATH  = "djangoenv\Lib\site-packages\osgeo\gdal304.dll"



