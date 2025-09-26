import os
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")  # Use Service Role Key
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_avatar(file_obj, filename: str, bucket_name: str = "avatars") -> str:
    """
    Uploads a Django InMemoryUploadedFile to Supabase Storage and returns public URL.
    """

    import time

    timestamp = int(time.time())
    filename = f"{timestamp}_{filename}"

    # Read the file content as bytes
    file_bytes = file_obj.read()

    # Upload the file bytes
    response = supabase.storage.from_(bucket_name).upload(filename, file_bytes)
    if response.get("error"):
        raise Exception(f"Supabase upload failed: {response['error']['message']}")

    # Return the public URL
    public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
    if public_url.get("error"):
        raise Exception(
            f"Supabase get_public_url failed: {public_url['error']['message']}"
        )

    return public_url["publicUrl"]
