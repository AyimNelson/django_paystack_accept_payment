from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import uuid
from datetime import datetime, timedelta
from django.utils import timezone


"""
Extend the default user model and add new attributes/fields to the user... 
You can handle profile fields here
This can include image, bio, social media handles(links) etc

"""

class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, blank=False, null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    # Add more user object fields
    
    
    # Authenticate user with email... Remove if not needed
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    
    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"pk": self.user_id})
    
    class Meta():
        ordering = ['-date_registered']