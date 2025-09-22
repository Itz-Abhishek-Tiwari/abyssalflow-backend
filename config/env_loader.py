from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.dev")
env_file = (
    BASE_DIR / ".env.prod"
    if "prod" in settings_module.lower()
    else BASE_DIR / ".env.dev"
)

load_dotenv(env_file)
