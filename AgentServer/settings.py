"""
Django settings for AgentServer project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from configparser import ConfigParser
from urllib.parse import urljoin
import random
import string
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/config.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = random.choices(string.ascii_letters + string.digits, k=50)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("debug", 'false') == 'true'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dongtai',
    'apiserver',
    'drf_spectacular'
]

#
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    # OTHER SETTINGS
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': ['django.core.paginator'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # swagger setting
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AgentServer.urls'

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

WSGI_APPLICATION = 'AgentServer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#if len(sys.argv) > 1 and sys.argv[1] == 'test':
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        }
#    }
#else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'charset': 'utf8mb4'
        },
        'USER': config.get("mysql", 'user'),
        'NAME': config.get("mysql", 'name'),
        'PASSWORD': config.get("mysql", 'password'),
        'HOST': config.get("mysql", 'host'),
        'PORT': config.get("mysql", 'port'),
        'TEST': {
            'OPTIONS': {
                'charset': 'utf8mb4'
            },
            'USER': config.get("mysql", 'user'),
            'NAME': config.get("mysql", 'name'),
            'PASSWORD': config.get("mysql", 'password'),
            'HOST': config.get("mysql", 'host'),
            'PORT': config.get("mysql", 'port'),
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'dongtai.User'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# 配置RSA加解密需要的公钥、私钥路径
PRIVATE_KEY = os.path.join(BASE_DIR, 'config', 'rsa_keys/private_key.pem')
PUBLIC_KEY = os.path.join(BASE_DIR, 'config', 'rsa_keys/public_key.pem')

ENGINE_URL = config.get("engine", "url")
HEALTH_ENGINE_URL = urljoin(ENGINE_URL, "/api/engine/health")
BASE_ENGINE_URL = config.get("engine", "url") + '/api/engine/run?method_pool_id={id}'
REPLAY_ENGINE_URL = config.get("engine", "url") + '/api/engine/run?method_pool_id={id}&model=replay'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} [{module}.{funcName}:{lineno}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'dongtai.openapi': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/openapi.log'),
            'backupCount': 5,
            'maxBytes': 1024 * 1024 * 10,
            'formatter': 'verbose',
            'encoding':'utf8',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'dongtai.openapi': {
            'handlers': ['console', 'dongtai.openapi'],
            'propagate': True,
            'level': 'INFO',
        },
        'dongtai-core': {
            'handlers': ['console', 'dongtai.openapi'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

TEST_RUNNER = 'test.NoDbTestRunner'

# 配置阿里云OSS访问凭证
ACCESS_KEY = config.get('aliyun_oss', 'access_key')
ACCESS_KEY_SECRET = config.get('aliyun_oss', 'access_key_secret')
BUCKET_URL = 'https://oss-cn-beijing.aliyuncs.com'
BUCKET_NAME = 'dongtai'
BUCKET_NAME_BASE_URL = 'agent/' if os.getenv('active.profile',
                                             None) != 'TEST' else 'agent_test/'
# CONST
PENDING = 1
VERIFYING = 2
CONFIRMED = 3
IGNORE = 4
SOLVED = 5
if os.getenv('active.profile', None) == 'TEST' or os.getenv('PYTHONAGENT', None) == 'TRUE':
    pass
    #MIDDLEWARE.append('dongtai_agent_python.middlewares.django_middleware.FireMiddleware')
