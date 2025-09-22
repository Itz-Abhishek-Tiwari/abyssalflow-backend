# backend/integrations/auth_backend.py
import os
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()
SUPABASE_URL = os.environ["SUPABASE_URL"]


class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            token = auth_header.split()[1]
        except Exception:
            return None

        # Use Supabase /auth/v1/user endpoint to validate token
        resp = requests.get(
            f"{SUPABASE_URL}/auth/v1/user", headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code != 200:
            raise exceptions.AuthenticationFailed("Invalid Supabase token")

        payload = resp.json()
        uid = payload.get("id") or payload.get("sub")
        if not uid:
            raise exceptions.AuthenticationFailed("Invalid supabase user")

        user, _ = User.objects.get_or_create(
            username=uid, defaults={"email": payload.get("email", "")}
        )
        return (user, None)
