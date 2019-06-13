from django.conf import settings


from django.db import models

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.db.models.signals import post_save
from entertainments.validators import image_validation_extension,video_validation_extention
#from plans.models import Option
#from plans.models import Plan


# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name}"#django refused to import this from plans

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    istream_options = models.ManyToManyField(Option, blank=True)
    photo = models.ImageField(upload_to='customer_profiles/',validators=[image_validation_extension])
    def __str__(self):
        return f"{self.user.username}, {self.photo}"

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = Profile.objects.get_or_create(user=instance)
    user_profile.save()
post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)