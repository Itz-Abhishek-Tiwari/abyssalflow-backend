from django.db import models
import uuid
from apps.files.models import FileUploadModel

# Choices for user roles
ROLE_CHOICES = [
    ("employee", "Employee"),
    ("manager", "Manager"),
    ("hr", "HR"),
    ("admin", "Admin"),
]

DEPARTMENT_CHOICES = []


class UserProfile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.CharField(
        max_length=100, blank=True, null=True
    )  # IT, HR, Admin, Management
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.full_name
