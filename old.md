
<!--# 📂 **Final Folder Structure – Detailed**

```
backend/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py              # Shared settings
│   │   ├── dev.py               # Local dev config
│   │   └── prod.py              # Prod config
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/                   # Supabase-authenticated users
│   │   ├── models.py            # Extend Django user (profiles)
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py          # Sync with Supabase user data
│   │   └── signals.py           # Profile auto-create on user sync
│   ├── employees/               # Employee profiles & roles
│   │   ├── models.py            # HR-specific info
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services.py
│   ├── tasks/                   # Task management
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services.py
│   ├── leaves/                  # Leave requests
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── services.py
│   ├── approvals/               # Approvals workflow
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── services.py
│   ├── chat/                    # Messaging via Supabase Realtime
│   │   ├── supabase_chat.py     # Wrapper for saving/querying
│   │   └── sync.py              # (optional) sync Supabase chats → Django
│   └── files/                   # File uploads (Supabase storage)
│       ├── supabase_storage.py
│       └── utils.py
├── integrations/                # Third-party integrations
│   ├── supabase_client.py       # Supabase SDK client
│   ├── auth_backend.py          # DRF authentication via Supabase JWT
│   ├── auth_sync.py             # Sync Supabase users <-> Django users
│   └── notifications.py         # Email/Slack/Push hooks
├── core/                        # Shared utilities
│   ├── permissions.py
│   ├── mixins.py
│   ├── exceptions.py
│   ├── pagination.py
│   └── utils.py
├── scripts/
│   ├── seed_data.py             # Generate dummy employees/tasks
│   ├── sync_supabase_users.py   # Batch sync job
│   └── nightly_reports.py       # Example cronjob
├── static/
├── media/
└── tests/
    ├── users/
    ├── employees/
    ├── tasks/
    ├── leaves/
    ├── approvals/
    ├── chat/
    └── files/
```

---

# 🔑 **Detailed Responsibilities**

| Feature                  | Django (Business Logic)                                                                              | Supabase (Infra)                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Auth**                 | - Uses Supabase JWT for all requests- Middleware verifies token- Optional: sync users into Django DB | - Handles sign up / login / password reset / OAuth- Issues JWTs |
| **Profiles / Employees** | - Employee model (designation, salary, HR info)- Profile enrichment beyond Supabase User             | - Stores basic user identity (email, UID)                       |
| **Tasks**                | - Task model, assignment, deadlines- Business rules: only managers assign tasks- Reporting           | - N/A                                                           |
| **Leaves**               | - Leave request model- Validation (balance, approvals)- Audit logs                                   | - N/A                                                           |
| **Approvals**            | - Approval workflows (leave, expense, promotion)- Multi-step logic                                   | - N/A                                                           |
| **Chat / Messaging**     | - Optional: archive messages for compliance                                                          | - Supabase Realtime handles live chat + subscriptions           |
| **Files**                | - Stores metadata (who uploaded, linked entity)- Maps file URLs into DB                              | - Supabase Storage handles upload, retrieval, public URLs       |
| **Notifications**        | - Business logic for when to notify                                                                  | - Can send via Supabase functions or Django + third-party       |

---

# ⚙️ **Core Integrations**

### **1. Supabase Auth in Django (DRF backend)**

`integrations/auth_backend.py`

```python
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from integrations.supabase_client import supabase

User = get_user_model()

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, options={"verify_signature": False})
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Supabase token")

        # Sync Supabase user into Django
        user, _ = User.objects.get_or_create(
            username=payload["sub"],
            defaults={"email": payload.get("email", "")}
        )
        return (user, None)
```

---

### **2. Supabase Storage Wrapper**

`apps/files/supabase_storage.py`

```python
from integrations.supabase_client import supabase

def upload_profile_pic(user_id: str, file_bytes: bytes):
    path = f"profiles/{user_id}.jpg"
    supabase.storage.from_("profile_pics").upload(path, file_bytes)
    return supabase.storage.from_("profile_pics").get_public_url(path)
```

---

### **3. Supabase Realtime Chat Wrapper**

`apps/chat/supabase_chat.py`

```python
from integrations.supabase_client import supabase

def send_message(room_id: str, sender_id: str, text: str):
    return supabase.table("messages").insert({
        "room_id": room_id,
        "sender_id": sender_id,
        "message": text
    }).execute()

def get_history(room_id: str):
    return supabase.table("messages").select("*").eq("room_id", room_id).execute()
```

---

# 🔗 **Frontend Flow (React Native + Supabase + Django)**

1. **User Login/Signup** → Supabase Auth SDK → receive JWT.
    
2. **Authenticated API Requests** → Send `Authorization: Bearer <JWT>` → Django verifies token.
    
3. **HR Features (employees, tasks, leaves, approvals)** → Call Django API.
    
4. **Chat** → React Native connects **directly** to Supabase Realtime.
    
5. **Files** → Upload to Supabase Storage → Save URL in Django DB.
    

---

# ✅ **Benefits of this Split**

- **Supabase covers infra** → Auth, Realtime, Storage = no heavy lifting.
    
- **Django covers business logic** → HR rules, workflows, reports = strong backend.
    
- **Scalable & Industry-standard** → Feature-based apps, integrations isolated, clean auth layer.
    
- **Easier DevOps** → Supabase reduces infra complexity, Django runs as an API service.
    
