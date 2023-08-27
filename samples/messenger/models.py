from django.db import models
from django.contrib.auth.models import User

class UserProfileImage(models.Model):
    userInstance = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_image')
    
    userImage = models.ImageField(upload_to='profile-images/', blank=True, null=True)
