from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
