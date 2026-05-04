"""
Django settings for bk_pg_management project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-5fk27j+++16a5+%gx7m%=(k(l35=62yo6ot+m1-b4apme-7v_f'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'jazzmin',   # ⭐ modern admin UI (must be first)

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pgapp',
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

ROOT_URLCONF = 'bk_pg_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 🔥 OPTIONAL (helps avoid template issues)
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bk_pg_management.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔥 Jazzmin UI settings
JAZZMIN_SETTINGS = {
    "site_title": "BK PG Admin",
    "site_header": "BK PG Management",
    "site_brand": "BK PG",

    "welcome_sign": "Welcome to BK PG Dashboard",
    "copyright": "BK PG",

    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
    ],

    "icons": {
        "pgapp.tenant": "fas fa-users",
        "pgapp.bed": "fas fa-bed",
        "pgapp.room": "fas fa-building",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
}

# 🔐 FIXED LOGIN SETTINGS
LOGIN_URL = '/login/'          # ✅ YOUR custom login page
LOGIN_REDIRECT_URL = '/'       # ✅ after login → dashboard
LOGOUT_REDIRECT_URL = '/login/'  # ✅ after logout → login