from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
class UserRegistration(models.Model):
    USER_TYPES = [
        ('NGO', 'NGO'),
        ('Corporation', 'Corporation'),
        ('Individual', 'Individual'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

class Post(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name="posts")
    
    # Existing field
    text = models.TextField()
    
    # New fields for analysis data
    sus = models.BooleanField(default=False)  # To store if the text aligns with sustainability
    sdg_names = ArrayField(models.CharField(max_length=50), blank=True, default=list)  # List of SDG names
    sdg_descriptions = ArrayField(models.TextField(), blank=True, default=list)  # List of SDG descriptions
    target_names = ArrayField(models.CharField(max_length=50), blank=True, default=list)  # List of target names
    target_descriptions = ArrayField(models.TextField(), blank=True, default=list)  # List of target descriptions
    sustainability_dimensions = JSONField(default=dict)  # JSON field to store sustainability dimensions

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at}"

class Partnership(models.Model):
    user = models.ForeignKey(UserRegistration, related_name='partnerships', on_delete=models.CASCADE)
    partner = models.ForeignKey(UserRegistration, related_name='partners', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted')])
    created_at = models.DateTimeField(auto_now_add=True)

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)

