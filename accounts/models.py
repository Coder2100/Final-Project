from django.conf import settings
from django.db import models

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
#importing from entertainment class
from entertainments.validators import image_validation_extension,video_validation_extention

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='customer_profiles/',validators=[image_validation_extension])
    def __str__(self):
        return f"{self.user.username}, {self.photo}"

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = Profile.objects.get_or_create(user=instance)
    user_profile.save()
post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)