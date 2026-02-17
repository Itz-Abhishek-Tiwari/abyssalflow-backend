# 🚀 Project Name

Enterprise-ready Modular Monolith built with **Django + DRF**.

This project follows a **Layered Architecture (Domain → Application → Infrastructure → Presentation)** to ensure:

* Scalability
* Team collaboration
* Future microservice extraction
* Clean separation of concerns
* Maintainability

---

# 🏗 Architecture Overview

```
apps/
    <domain>/
        domain/         # Pure business logic
        application/    # Use cases
        infrastructure/ # DB, external systems
        presentation/   # DRF views, serializers
        tests/

core/
    common/             # Shared utilities
    infrastructure/     # Global infra configs
    tasks/              # Background jobs

integrations/
    supabase/
    auth/
    notifications/

api/
    v1/

config/
    settings/
```

---

# 🧠 Architectural Principles

## 1️⃣ Modular Monolith

Each domain (users, employees, leaves, etc.) is isolated and self-contained.

## 2️⃣ Layered Design

### Domain Layer

* Business rules
* No external API calls
* No DRF logic

### Application Layer

* Use cases
* Orchestration
* Calls repositories and integrations

### Infrastructure Layer

* DB access
* Supabase
* External APIs
* Email
* Storage

### Presentation Layer

* DRF Views
* Serializers
* HTTP handling

---

# 🔌 Integrations

External services are isolated under:

```
integrations/
```

This prevents infrastructure leakage into business logic.

---

# 🔄 API Versioning

All APIs are versioned:

```
/api/v1/
```

This prevents breaking frontend/mobile clients in the future.

---

# 🧪 Testing Strategy

Each app contains its own tests:

```
apps/<domain>/tests/
```

Test levels:

* Unit tests (domain)
* Service tests (application)
* API tests (presentation)

---

# 🛠 Local Development

### 1️⃣ Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Environment

Create `.env`:

```
DEBUG=True
SECRET_KEY=your-secret
DATABASE_URL=postgres://...
```

### 3️⃣ Run

```bash
python manage.py migrate
python manage.py runserver
```

---

# 🏭 Production Notes

* Use PostgreSQL
* Enable structured logging
* Configure Sentry
* Use Redis + Celery for background tasks
* Use Gunicorn + Nginx

---

# 🔮 Future Roadmap

Because of strict boundaries, modules can be extracted into microservices later:

* leave-service
* task-service
* chat-service

Without rewriting business logic.

---

# 👥 Contributing

Follow these rules:

* No cross-app direct imports
* No business logic inside views
* No external API calls inside domain layer
* Always create use-cases in application layer

---

# 📄 License

MIT
