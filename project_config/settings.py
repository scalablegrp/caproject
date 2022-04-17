import os
import dj_database_url

# Import the file that has the environment variables
if os.path.exists("env.py"):
    import env as env_variables

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [*,]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django-extensions', # this wil lallow secure certficate over localhost
    'storages', #this will allow use of S3Boto3 storage
    'home',
    'user_auth',
    'property',
    'bid',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_config.urls'

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
                # Context Processor to determine if user is logged in on each page
                'user_auth.contexts.determine_if_logged_in',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_config.wsgi.application'

 #If there is a environment variable for the database use that databases details
if os.path.exists("env.py"):
    DATABASES = {
        'default':  dj_database_url.parse(env_variables.get_db_url())
    }
else:
    DATABASES = {
        'default':  dj_database_url.parse(os.environ.get('db_url'))
    }


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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # This may need to be changed


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# S3 Details Retrieved from environment variables
if os.path.exists("env.py"):
    AWS_ACCESS_KEY_ID = env_variables.get_aws_access_key("")
    AWS_SECRET_ACCESS_KEY = env_variables.get_aws_secret_key("")
    AWS_STORAGE_BUCKET_NAME = env_variables.get_bucket_name()
    IMAGE_BUCKET_URL = env_variables.get_s3_url()
    STRIPE_PUBLISHABLE_KEY = env_variables.get_stripe_publishable()
    STRIPE_SECRET_KEY = env_variables.get_stripe_secret()
# Retrieve environment variables from os if .env file not available
else:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    IMAGE_BUCKET_URL = os.environ.get('IMAGE_BUCKET_URL')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    