import os

DEBUG = False

ALLOWED_HOSTS = ["starnavi-test-project.herokuapp.com", "localhost",
                 "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DATABASE_NAME", "postgres"),
        'USER': os.environ.get("DATABASE_USER", "postgres"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD", "postgres"),
        'HOST': os.environ.get("DATABASE_HOST", "localhost"),
        'CONN_MAX_AGE': 60,
    }
}
