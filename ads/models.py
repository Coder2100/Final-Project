from django.db import models
from entertainments.validators import image_validation_extension,video_validation_extention
# Create your models here.
class BurnerSlide(models.Model):
    heading = models.CharField(max_length=30)#pricise
    background_image = models.ImageField(upload_to='customer_profiles/',validators=[image_validation_extension])
    main_message = models.TextField()
    button_message = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.heading}, {self.background_image}, {self.main_message}, {self.button_message}"

    def get_absolute_url(self):
        return reverse('ads:index')

class TrendingAd(models.Model):
    circle_title = models.CharField(max_length=40)#pricise
    #background_image = models.ImageField(upload_to='customer_profiles/',validators=[image_validation_extension])
    heading = models.CharField(max_length=30)#pricise
    content = models.TextField()
    button_message = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.circle_title}, {self.heading}, {self.content}, {self.button_message}"

    def get_absolute_url(self):
        return reverse('ads:index')

class Story(models.Model):
    headline = models.CharField(max_length=140)#pricise
    cover_image = models.ImageField(upload_to='customer_profiles/',validators=[image_validation_extension])
    content = models.TextField()
    #button_message = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.headline}, {self.cover_image}, {self.content}"

    def get_absolute_url(self):
        return reverse('ads:index')

class Footer(models.Model):
    left = models.TextField()
    right = models.TextField()
    center = models.TextField()

    def __str__(self):
        return f"{self.left}, {self.right}, {self.center}"#dividing the footer 

