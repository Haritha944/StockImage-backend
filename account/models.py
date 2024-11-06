from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['phone_number']  
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_user_groups', 
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.email
   