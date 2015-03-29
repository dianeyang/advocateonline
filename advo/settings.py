"""
Django settings for advo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "iwdq=bgnj2tsp*uc2(_kd59!0724wrkf(@m9$g0^7rds)jgruj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'ajax_select',
    'south',
    'magazine',
    'blog',
    'payments',
    'django_social_share',
    'contacts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'advo.urls'

WSGI_APPLICATION = 'advo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'advocate',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    #http://stackoverflow.com/questions/3756841/django-media-url-blank    
    'django.core.context_processors.media',
)

AJAX_LOOKUP_CHANNELS = {
     'contributor' : ('magazine.lookups', 'ContributorLookup'),
     'tag' : ('magazine.lookups', 'TagLookup'),
}

STRIPE_BUY_PUBLIC_KEY = os.environ.get("STRIPE_BUY_PUBLIC_KEY", "pk_test_7mkjcG8fQj3qmdhCgP92Pq4g")
STRIPE_DONATE_PUBLIC_KEY = os.environ.get("STRIPE_DONATE_PUBLIC_KEY", "pk_test_66u2FQCcD717Ot7UGj1IvEsN")

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'paste_retain_style_properties': "color font-size",
    'content_css': "/static/magazine/css/tinymce_custom.css", 
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

try:
    from local_settings import *
except ImportError:
    pass
