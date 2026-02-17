
#!/bin/bash

echo "🚨 Backing up current project..."
cp -r . ../project_backup_$(date +%Y%m%d_%H%M%S)

echo "📁 Creating new layered structure..."

# Create base directories
mkdir -p api/v1
mkdir -p core/common
mkdir -p core/infrastructure
mkdir -p core/tasks

mkdir -p integrations/supabase
mkdir -p integrations/auth
mkdir -p integrations/notifications

# Function to restructure app
restructure_app () {
  APP_NAME=$1

  echo "🔄 Restructuring $APP_NAME..."

  mkdir -p apps/$APP_NAME/domain
  mkdir -p apps/$APP_NAME/application
  mkdir -p apps/$APP_NAME/infrastructure
  mkdir -p apps/$APP_NAME/presentation
  mkdir -p apps/$APP_NAME/tests

  # Move files safely
  [ -f apps/$APP_NAME/models.py ] && mv apps/$APP_NAME/models.py apps/$APP_NAME/domain/
  [ -f apps/$APP_NAME/services.py ] && mv apps/$APP_NAME/services.py apps/$APP_NAME/domain/
  [ -f apps/$APP_NAME/serializers.py ] && mv apps/$APP_NAME/serializers.py apps/$APP_NAME/presentation/
  [ -f apps/$APP_NAME/views.py ] && mv apps/$APP_NAME/views.py apps/$APP_NAME/presentation/
  [ -f apps/$APP_NAME/urls.py ] && mv apps/$APP_NAME/urls.py apps/$APP_NAME/presentation/
  [ -f apps/$APP_NAME/signals.py ] && mv apps/$APP_NAME/signals.py apps/$APP_NAME/infrastructure/
  [ -f apps/$APP_NAME/admin.py ] && mv apps/$APP_NAME/admin.py apps/$APP_NAME/infrastructure/
  [ -f apps/$APP_NAME/tests.py ] && mv apps/$APP_NAME/tests.py apps/$APP_NAME/tests/

}

# Restructure each domain app
restructure_app "users"
restructure_app "employees"
restructure_app "leaves"
restructure_app "tasks"
restructure_app "approvals"

echo "📦 Moving Supabase integrations..."

[ -f apps/chat/supabase_chat.py ] && mv apps/chat/supabase_chat.py integrations/supabase/chat.py
[ -f apps/files/supabase_storage.py ] && mv apps/files/supabase_storage.py integrations/supabase/storage.py
[ -f integrations/supabase_client.py ] && mv integrations/supabase_client.py integrations/supabase/client.py

echo "🔐 Moving auth integrations..."

[ -f integrations/auth_backend.py ] && mv integrations/auth_backend.py integrations/auth/backend.py
[ -f integrations/auth_sync.py ] && mv integrations/auth_sync.py integrations/auth/sync.py

echo "📨 Moving notification integrations..."

[ -f integrations/notifications.py ] && mv integrations/notifications.py integrations/notifications/email.py

echo "🧹 Cleaning old structure (empty folders only)..."
find apps -type d -empty -delete

echo "✅ Restructure complete."
echo "⚠️  Now manually fix imports."