"""
Django settings for config project - Local Development Configuration
Extends base.py with development-specific settings.
"""

from .base import *  # noqa

# ═════════════════════════════════════════════════════════════════════════════
# DEBUG & SECURITY
# ═════════════════════════════════════════════════════════════════════════════

DEBUG = True
ALLOWED_HOSTS = ['*']

# ═════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE - DEVELOPMENT
# ═════════════════════════════════════════════════════════════════════════════

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ═════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT APPS
# ═════════════════════════════════════════════════════════════════════════════

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# ═════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═════════════════════════════════════════════════════════════════════════════

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# REST FRAMEWORK - DEVELOPMENT
# ═════════════════════════════════════════════════════════════════════════════

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',  # For development API browsing
]

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.AllowAny',  # Allow unauthenticated access in development
]

# ═════════════════════════════════════════════════════════════════════════════
# SPECTACULAR SETTINGS (API DOCUMENTATION)
# ═════════════════════════════════════════════════════════════════════════════

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Login API',
    'DESCRIPTION': 'Industry-standard Django API',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SCHEMA_PATH_PREFIX': '/api/v1/',
    'AUTHENTICATION_FLOWS': {
        'bearer': {
            'type': 'http',
            'scheme': 'bearer',
        },
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# CORS - DEVELOPMENT (Allow all)
# ═════════════════════════════════════════════════════════════════════════════

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

# ═════════════════════════════════════════════════════════════════════════════
# EMAIL CONFIGURATION (Console backend for development)
# ═════════════════════════════════════════════════════════════════════════════

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ═════════════════════════════════════════════════════════════════════════════
# LOGGING - DEVELOPMENT
# ═════════════════════════════════════════════════════════════════════════════

LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['apps']['level'] = 'DEBUG'

# ═════════════════════════════════════════════════════════════════════════════
# SECURITY - RELAXED FOR LOCAL DEVELOPMENT
# ═════════════════════════════════════════════════════════════════════════════

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_BROWSER_XSS_FILTER = True

# ═════════════════════════════════════════════════════════════════════════════
# CACHE - DEVELOPMENT (Simple in-memory cache)
# ═════════════════════════════════════════════════════════════════════════════

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'django-login-cache',
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# SHELL PLUS SETTINGS (Django Extensions)
# ═════════════════════════════════════════════════════════════════════════════

SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_LOCATION = 'bottom'
