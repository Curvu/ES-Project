from django.db import models

class Token(models.Model):
    token = models.TextField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.token}"
