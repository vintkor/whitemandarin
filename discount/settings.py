"""
Django settings for discount project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8^g=0ma4d)i7!p$(i0fvulmra+)1yz@urt+don(4$v!ds2v$)c'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
AUTH_USER_MODEL = 'profile.User'
# ACCOUNT_AUTHENTICATION_METHOD = ("email",)


SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['20kn.gowius.com', '127.0.0.1']

ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = "/"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Application definition

ADMIN_ACCESS_WHITELIST_ENABLED = True
ADMIN_ACCESS_WHITELIST_MESSAGE = "Site is underconstruction"

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'tinymce',
    'shop',
    'easy_thumbnails',
    'image_cropping',
    'fileupload',
    'content',
    'profile',
    'redactor',
    'slideshow',
    'pricelist',
    # 'sorl.thumbnail',
    # 'admin_ip_whitelist',

     # The Django sites framework is required
    'django.contrib.sites',
    'hotline',
    'comments',
    'raiting',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # # 'allauth.socialaccount.providers.odnoklassniki',
    # # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.vk',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',

    # 'admin_ip_whitelist.middleware.AdminAccessIPWhiteListMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'action.middleware.setDefaultCityMiddleware'
    'shop.middleware.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',


]

ROOT_URLCONF = 'discount.urls'

WSGI_APPLICATION = 'discount.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'discount', 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'whitemandarin',
        'USER': 'whitemandarin',
        'PASSWORD': 'yGfdSwqa654VxJd',
        'HOST': '91.121.71.107',
        'PORT': '5432',
    },
   # 'mysql': {
   #     'ENGINE': 'django.db.backends.mysql',
   #     'NAME': '20knlast',
   #     'USER': 'root',
   #     'PASSWORD': 'root',
   #     'HOST': '127.0.0.1',
   #     'PORT': '8889',
   # },
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_URL = ''
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# # assert False, PROJECT_ROOT
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# # assert False, STATIC_ROOT
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, "static"),
# )
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static_cdn/'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
    # '/var/www/static/',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')

# assert False, STATIC_ROOT

# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
DEFAULT_FROM_EMAIL = 'info@lukoshkino.com.ua'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'info@lukoshkino.com.ua'
EMAIL_HOST_PASSWORD = 'iloveJ10'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TINYMCE_JS_URL = STATIC_URL + "tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = STATIC_ROOT + "/tiny_mce"


TINYMCE_SPELLCHECKER=False

TINYMCE_PLUGINS = [
    'safari',
    'table',
    'advlink',
    'advimage',
    'iespell',
    'inlinepopups',
    'media',
    'searchreplace',
    'contextmenu',
    'paste',
    'wordcount'
]

TINYMCE_DEFAULT_CONFIG={
    'theme' : "advanced",
    'plugins' : ",".join(TINYMCE_PLUGINS), # django-cms
    'language' : 'ru',
    "theme_advanced_buttons1" : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect,|,spellchecker",
    "theme_advanced_buttons2" : "cut,copy,paste,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image,cleanup,code,|,forecolor,backcolor,|,insertfile,insertimage",
    "theme_advanced_buttons3" : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : True,
    'table_default_cellpadding': 2,
    'table_default_cellspacing': 2,
    'cleanup_on_startup' : False,
    'cleanup' : False,
    'paste_auto_cleanup_on_paste' : False,
    'paste_block_drop' : False,
    'paste_remove_spans' : False,
    'paste_strip_class_attributes' : False,
    'paste_retain_style_properties' : "",
    'forced_root_block' : False,
    'force_br_newlines' : False,
    'force_p_newlines' : False,
    'remove_linebreaks' : False,
    'convert_newlines_to_brs' : False,
    'inline_styles' : False,
    'relative_urls' : False,
    'formats' : {
        'alignleft' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-left'},
        'aligncenter' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-center'},
        'alignright' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-right'},
        'alignfull' : {'selector' : 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', 'classes' : 'align-justify'},
        'strikethrough' : {'inline' : 'del'},
        'italic' : {'inline' : 'em'},
        'bold' : {'inline' : 'strong'},
        'underline' : {'inline' : 'u'}
    },
    'pagebreak_separator' : "",
    # Drop lists for link/image/media/template dialogs
    'template_external_list_url': 'lists/template_list.js',
    'external_link_list_url': 'lists/link_list.js',
    'external_image_list_url': 'lists/image_list.js',
    'media_external_list_url': 'lists/media_list.js',
    #
    #'file_browser_callback':'tinyDjangoBrowser'
}

DEFAULT_FROM_EMAIL = '20Klogin@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '20Klogin@gmail.com'
EMAIL_HOST_PASSWORD = '20kcheckin'
EMAIL_PORT = 587

IMAGE_UPLOAD_DIR = 'img'

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

IMAGE_CROPPING_THUMB_SIZE = (1300, 1300)

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# For 1.3 and development version add:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

