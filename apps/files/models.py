from django.db import models


def upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp"]

    if ext in image_extensions:
        return f"images/{filename}"
    else:
        return f"files/{filename}"


class FileUploadModel(models.Model):
    file = models.ImageField(upload_to=upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_at
