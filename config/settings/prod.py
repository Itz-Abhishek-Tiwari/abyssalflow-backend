import os
import dj_database_url
from .base import *  # noqa

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"), conn_max_age=600, ssl_require=True
    )
}
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "127.0.0.1,localhost,abyssalflow-backend.onrender.com"
).split(",")


DEBUG = False
