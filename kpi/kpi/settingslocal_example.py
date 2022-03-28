import os
import pathlib
from pathlib import Path


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key'

DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']
ADMIN_PATH = 'admin'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'unical_accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'sass_processor',

    # 'rest_framework',
    # 'rest_framework.authtoken',
    # 'corsheaders',

    'organizational_area',
    'visiting_management',


    'django_unical_bootstrap_italia',
    'bootstrap_italia_template',
    'template',

    'ajax_datatable',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = "unical_accounts.User"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'it-it'
LANGUAGE = LANGUAGE_CODE.split('-')[0]
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# GETTEXT LOCALIZATION
MIDDLEWARE.append('django.middleware.locale.LocaleMiddleware')
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
#
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
DATA_DIR = os.path.join(BASE_DIR, "data")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
if not os.path.exists(STATIC_ROOT):
    pathlib.Path(STATIC_ROOT).mkdir(parents=True, exist_ok=True)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    pathlib.Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)


# REST FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',  # dev server
    # add deploy server
    # add front-end server
]

# custom date/datetime format
DEFAULT_DATE_FORMAT = '%d/%m/%Y'
DEFAULT_TIME_FORMAT = '%H:%M'
DEFAULT_DATETIME_FORMAT = f'{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}'

# override globals
DATE_INPUT_FORMATS = ['%Y-%m-%d', DEFAULT_DATE_FORMAT]
DATETIME_INPUT_FORMATS = [DEFAULT_DATETIME_FORMAT,
                          f'%Y-%m-%d {DEFAULT_TIME_FORMAT}']
