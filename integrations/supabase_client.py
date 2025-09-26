import os
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")  # Use Service Role Key
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_avatar(file_obj, filename):
    bucket_name = "avatars"
    import time

    filename = f"{int(time.time())}_{filename}"

    supabase.storage.from_(bucket_name).upload(filename, file_obj)
    url = supabase.storage.from_(bucket_name).get_public_url(filename)
    return url
