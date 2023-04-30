"""
Django settings for my_blog project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import socket
import os
import dj_database_url

from pathlib import Path

from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='foo')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))
print(DEBUG)

ALLOWED_HOSTS = [] if DEBUG else os.environ.get("ALLOWED_HOSTS").split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',  # whitenoise
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Local apps
    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',

    # Third party apps
    'taggit',
    'django.contrib.postgres',
    'ckeditor',

    # the social providers
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
]
if DEBUG == True:
    INSTALLED_APPS.extend(['debug_toolbar'])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
if DEBUG:
    MIDDLEWARE.extend(['debug_toolbar.middleware.DebugToolbarMiddleware',])

ROOT_URLCONF = 'my_blog.urls'

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
                'blog.views.inject_form'  # custom search form processor
            ],
        },
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]


# STATICFILES_FINDERS = [
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BAACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # django allauth config
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'blog:home'
ACCOUNT_LOGOUT_REDIRECT = 'blog:home'


SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

# django-debug-toolbar
if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    print(ips)
    INTERNAL_IPS = ['127.0.0.1'] + [ip[:-1] + "1" for ip in ips]

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# if DEBUG == 1:
#     EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# else:
#     EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# whitenoise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
