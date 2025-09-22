from django.db import models
from .constants import PRIORITY_CHOICE, STATUS_CHOICE


class Task(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICE,
        default=STATUS_CHOICE[0][0],
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICE,
        default=PRIORITY_CHOICE[0][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=400, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    progress = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
    )
    assigned_to = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
