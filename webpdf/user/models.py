from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')