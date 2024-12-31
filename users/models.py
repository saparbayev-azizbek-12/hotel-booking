from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    image = models.FileField(upload_to='images/')
    phone_number = models.CharField(max_length=35, blank=True, null=True)

    def __str__(self):
        return self.username