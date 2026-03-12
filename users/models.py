from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    social_links = models.JSONField(default=dict, blank=True)
    is_verified_instructor = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_instructor(self):
        return self.role == 'instructor' or self.is_verified_instructor
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_platform_admin(self):
        return self.role == 'admin' or self.is_superuser
