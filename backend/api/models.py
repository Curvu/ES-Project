from django.db import models
from django.utils import timezone

class Users(models.Model):
    username = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Token(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.token} - {self.is_valid}"
