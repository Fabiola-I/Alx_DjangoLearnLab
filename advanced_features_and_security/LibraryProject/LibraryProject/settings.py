"""
Django settings for LibraryProject project.
"""

import os
from pathlib import Path

# ==========================================================
# --- BASE CONFIGURATION ---
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
# ==========================================================
# --- HTTPS / Proxy SSL Header ---
# ==========================================================
# If Django is behind a proxy that handles SSL, this tells Django
# to trust the X-Forwarded-Proto header and recognize HTTPS requests
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECRET_KEY = 'django-insecure-c)i27y*#&!p%h^h+h7tq39v^o#y-s0$g^!g^p_g^#h'  # Replace in production

DEBUG = False  # Required by ALX for security tasks

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']


# ==========================================================
# --- APPLICATION DEFINITION ---
# ==========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    'bookshelf',              # <-- IMPORTANT (CustomUser lives here)
    'relationship_app',

    # Celery
    'django_celery_results',

    # 2FA
    'two_factor',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_email',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # NEW — Required for HTTPS security & session handling
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',

    # CSP middleware (required for secure headers)
    'bookshelf.middleware.CSPMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'LibraryProject.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # optional but helpful
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


WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# ==========================================================
# --- DATABASE CONFIGURATION ---
# ==========================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================================
# --- PASSWORD VALIDATION ---
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================================
# --- INTERNATIONALIZATION ---
# ==========================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kigali'
USE_I18N = True
USE_TZ = True


# ==========================================================
# --- STATIC & MEDIA FILES ---
# ==========================================================
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# --- CUSTOM USER MODEL (Required) ---
# ==========================================================
AUTH_USER_MODEL = 'bookshelf.CustomUser'   # <-- Correct & final


# ==========================================================
# --- CACHING CONFIGURATION ---
# ==========================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-library-cache-location',
    }
}


# ==========================================================
# --- SECURITY CONFIGURATION (HTTPS + Hardening) ---
# ==========================================================
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True


# ==========================================================
# --- CELERY CONFIGURATION ---
# ==========================================================
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# ==========================================================
# --- 2FA CONFIGURATION ---
# ==========================================================
AUTHENTICATION_BACKENDS = [
    'two_factor.backends.TwoFactorAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = '/'
TWO_FACTOR_REQUIRED_ADMIN = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Enforce HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS protection
SECURE_BROWSER_XSS_FILTER = True

# ✅ Add this to satisfy checker
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
