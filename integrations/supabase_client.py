# backend/integrations/supabase_client.py
import os
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]  # server-only
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
