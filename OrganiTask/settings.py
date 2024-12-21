from datetime import timedelta
import os
from decouple import config
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}


# For local development, if DB is not yet set up, you can use SQLite:
if not config('DB_NAME', default=None):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# Other configurations (static files, media files, etc.) go here...



AUTH_USER_MODEL = 'users.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',  # JWT support
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',  # If CORS is needed
    'OrganizeMe',
    'OrganizeMe.users',  # The 'users' app
    'OrganizeMe.tasks',  # The 'tasks' app
    'OrganizeMe.notes',  # The 'notes' app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# Allow requests from any domain for testing (for production, be more specific)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['https://drf-api-n9oj.onrender.com']



ALLOWED_HOSTS = ['https://drf-api-n9oj.onrender.com', '127.0.0.1', 'render.com']

# Security settings
CSRF_TRUSTED_ORIGINS = [
    "https://drf-api-n9oj.onrender.com",
]





# Allow specific HTTP methods (e.g., POST, GET) if needed
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# If you're using `POST`, `PUT`, or other methods with non-simple headers, you might also need to allow `Access-Control-Allow-Headers`:
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-requested-with',
    'accept',
    'origin',
    'user-agent',
    'x-csrftoken',
]

ROOT_URLCONF = 'OrganiTask.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'OrganiTask.wsgi.application'


from decouple import config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL
        'NAME': config('DB_NAME'),  # Database name from .env
        'USER': config('DB_USER'),  # Database user from .env
        'PASSWORD': config('DB_PASSWORD'),  # Database password from .env
        'HOST': config('DB_HOST', default='localhost'),  # Database host (default to 'localhost')
        'PORT': config('DB_PORT', cast=int, default=5432),  # PostgreSQL default port (default to 5432)
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # Testing Email in Console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use SMTP for real emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Enables SMTP for sending emails
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your email provider's SMTP host, e.g., 'smtp.gmail.com' for Gmail
EMAIL_PORT = 587  # Standard port for STARTTLS
EMAIL_USE_TLS = True  # Enables encryption
EMAIL_HOST_USER = 'frilancer029@gmail.com'  # Replace with your actual email address
EMAIL_HOST_PASSWORD = 'xcqv dedl qget cquo'  # Replace with your email account password or app-specific password





REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWT for authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Enforce authentication
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Access token valid for 30 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token valid for 1 day
    'ROTATE_REFRESH_TOKENS': False,  # Set to True to rotate refresh tokens on each use
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),  # Use 'Bearer' prefix for tokens
    'ALGORITHM': 'HS256',  # Token signing algorithm
}


