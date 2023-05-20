# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "recr_db",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": 25432,
    }
}