import os
import dj_database_url
from .base import *  # noqa

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"), conn_max_age=600, ssl_require=True
    )
}
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "127.0.0.1,localhost,abyssalflow-backend.onrender.com"
).split(",")


DEBUG = True
