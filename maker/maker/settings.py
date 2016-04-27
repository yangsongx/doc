#coding:utf-8
"""
Django settings for maker project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import re
import commands

#########################################################
# An util for dev env and product env check
#
# return value:
#  * 0 - a plain local dev(using SQLite)
#  * 1-  formal product server env(Using MySQL in formal server)
#  * 2 - My(ysx) local dev env(MySQL in LAN)
#  * ? - anyone can add here for your own dev type
def _check_env_type():
    env_type = 0

    s = commands.getoutput('who am i')
    if re.search(r'yang', s) != None:
        s = commands.getoutput('hostname')
        if re.search(r'debian', s) == None:
            return 2 # ysx dev env, for Ubuntu Virtual Machine

    return env_type

def is_ksyun_server():
    str=commands.getoutput("/sbin/ifconfig")
    return re.search("10.128", str)
import urllib2
def set_proxy():
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://10.128.16.44:800'})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

def set_ffmpeg_env():
    os.environ["PATH"]=BASE_DIR+"/tools/:"+ os.environ["PATH"]

# ks yun server, django will be launched by apache,
# it will follow the context of apache process, so we need to set http_proxy
if is_ksyun_server() != None:
    set_proxy()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9&7g$^rgo&6v&e445f(f^gdpk=uq7o*y-fvq$cys323ig3257$'

#add ffmpeg to PATH
set_ffmpeg_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CAREDEAR_DEBUG_MODE = True


ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
#'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webviews',
    'django_user_agents',
    'compressor',
    'django_mobile',
    'mathfilters',
    'uc', # User Center
    'home',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #'cas.middleware.CASMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'cas.backends.CASBackend',
)
# if is_ksyun_server()!=None:
#     CAS_SERVER_URL = 'http://login.botdocker.com/cas/'
# else:
#     CAS_SERVER_URL = 'http://login.botdocker.com:9999/cas/'
# CAS_LOGOUT_COMPLETELY = True
# CAS_PROVIDE_URL_TO_LOGOUT = True


# CAS_RESPONSE_CALLBACKS = (
#                  'webviews.views.cas_response',
#              )

ROOT_URLCONF = 'maker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        #'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mobile.context_processors.flavour',
            ],
            'loaders':[
                'django_mobile.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'maker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if _check_env_type() == 1:
  #TODO formal DB settings are????
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'botdocker',
        'USER': 'admin',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': True,

    }
  }
elif _check_env_type() == 2:
  #ysx dev DB env
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xyz',
        'USER': 'root',
        'PASSWORD': 'nanjing@!k',
        'HOST': '192.168.1.13',
        'PORT': '',
        'ATOMIC_REQUESTS': True,

    }
  }
else: # TODO - anyone can add your own DB based on @_check_env_type()
  # This is for Non-MySQL dev case
  DATABASES = {
    'default': {
       # 'ENGINE': 'django.db.backends.sqlite3',
       # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       # 'ATOMIC_REQUESTS': True,

       'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maker',
        'USER': 'root',
        'PASSWORD': 'robotlite@8',
        'HOST': 'www.ioniconline.com',
        'PORT': '33060',
        'ATOMIC_REQUESTS': True,


    }
  }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'zh_CN'

# changed by Yangsongxiang(use the local server's timezone setting)
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-hans'
AJAXIMAGE_AUTH_TEST = lambda u: True

USE_I18N = True

USE_L10N = True

# changed by Yangsongxiang(Ture --> False), use server's local time zone
# don't let django input any timezone related info
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
TEMPLATE_DIRS=(
    os.path.join(BASE_DIR, "templates"),
)
#STATICFILES_DIRS=(
#    os.path.join(BASE_DIR, "static"),
#    )


import sys
sys.path.append(os.path.join(BASE_DIR,"celery_handlers"))
CELERY_IMPORTS=(sys.path.append(os.path.join(BASE_DIR,"webviews/task")))

STATIC_ROOT = os.path.join(BASE_DIR, "static")
    
STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    ('css',os.path.join(STATIC_ROOT,'css').replace('\\','/') ),
#    ('js',os.path.join(STATIC_ROOT,'js').replace('\\','/') ),
#    ('images',os.path.join(STATIC_ROOT,'images').replace('\\','/') ),
#    ('fonts',os.path.join(STATIC_ROOT,'fonts').replace('\\','/') ),
#)


#for django useragent , disable it as of now
if is_ksyun_server() != None:
    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'yz-memcache1:11211',
        }
    }
else:
    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        }
    }


USER_AGENTS_CACHE = 'None'

if is_ksyun_server() != None:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/opt/maker/env/maker/logs/django.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers':['file'],
                'propagate': True,
                'level':'DEBUG',
            },
            'webviews': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': './logs/django.log',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers':['file'],
                'propagate': True,
                'level':'DEBUG',
            },
            'uc': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'webviews': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    }

PAGINATE_NUMBER = 10
LOGIN_URL = '/uc/login/'

EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'help@botdocker.com'
EMAIL_HOST_PASSWORD = 'Robot@Lite'
EMAIL_USE_TLS = False

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
)

GRAPPELLI_ADMIN_TITLE='21KE定制资源管理系统'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OFFLINE_CONTEXT = {
    'path_to_files': '/static/js/',
}
if CAREDEAR_DEBUG_MODE:
    COMPRESS_ENABLED = False
else:
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True

