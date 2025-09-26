# integrations/supabase_client.py

import os
import time
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception(
        "Supabase environment variables missing! "
        "Ensure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_avatar(file_obj, filename: str, bucket_name: str = "avatars") -> str:
    """
    Uploads a Django InMemoryUploadedFile to Supabase Storage and returns public URL.
    Compatible with latest supabase-py 3.x
    """

    # Add timestamp to filename to avoid collisions
    timestamp = int(time.time())
    filename = f"{timestamp}_{filename}"

    # Read file content as bytes
    file_bytes = file_obj.read()

    # Upload the file
    upload_resp = supabase.storage.from_(bucket_name).upload(
        path=filename, file=file_bytes
    )
    if not upload_resp.success:
        raise Exception(f"Supabase upload failed: {upload_resp.error.message}")

    # Get public URL
    public_url_resp = supabase.storage.from_(bucket_name).get_public_url(filename)
    if public_url_resp.error:
        raise Exception(
            f"Supabase get_public_url failed: {public_url_resp.error.message}"
        )

    return public_url_resp.public_url
