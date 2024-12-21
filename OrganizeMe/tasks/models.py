from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task: {self.title} (Priority: {self.priority})"

    class Meta:
        ordering = ['priority']  # Order tasks by priority (high -> low)

