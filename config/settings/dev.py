from .base import *  # noqa
import os

# ENV=local SQLite database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DEBUG = "True"  # cast to bool
