from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=255, unique=True)
    face_id = models.CharField(max_length=255, default=None)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username