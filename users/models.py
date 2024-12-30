from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=35, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Profile(CustomUser):
    img = models.FileField(upload_to="images/")

    class Meta:
        verbose_name_plural = 'Profile'