from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.URLField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    bio = models. TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    

# Create your models here.
