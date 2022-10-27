from pathlib import Path
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$iu+h%$a745fag_*v$jtr*%mx@r8yf5_7b3&mv%$rfn*g6#b1c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    'rest_framework',
    'rest_framework_api_key',
    'corsheaders',
    # My apps
    'sign',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ]
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

CORS_ALLOWED_ORIGINS = [
    "https://alstratech.com",
    "http://alstratech.com",
    "https://app.alstratech.com",
    "http://app.alstratech.com",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    'x_api_key',
]
CSRF_TRUSTED_ORIGINS = [
    "https://alstratech.com",
    "http://alstratech.com",
    "https://app.alstratech.com",
    "http://app.alstratech.com",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:9000",
]

# ========== ↓ PRIVATE IDS ↓ ==========
# Docusign
# ↓ Alstra developer keys ↓
CLIENT_AUTH_ID = 'ddc5199b-cfc5-4f6c-a33d-abac5a8fc9ea'  # Settings -> Integrations -> Apps and keys -> Integration Key
CLIENT_USER_ID = 'e84a3846-339c-47f5-9eb9-eb2646f7b389'  # Settings -> Integrations -> Apps and keys -> API User ID
ACCOUNT_ID = '14fc73b4-b3b5-482c-9cb1-dca05202f29b'  # Settings -> Integrations -> Apps and keys -> API Account ID
# ↑ Alstra developer keys ↑
# ========== ↑ PRIVATE IDS ↑ ==========