from django.conf import settings

from django.db import models
from django.urls import reverse

from .validators import image_validation_extension,video_validation_extention

from datetime import datetime

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

FILM_CHOICES = (
    ('D', 'Drama'),
    ('S', 'Sitcom'),
    ('PD', 'Podcast Video'),
    ('SR', 'Series'),
    ('RS', 'Reality TV Show'),
    ('H', 'Home Entertainment')
)

PODCAST_CHOICES = (
    ('L', 'Life Advice'),
    ('F', 'Personal Finance'),
    ('A', 'Academic Performance'),
    ('O', 'Other')
)

SONG_CHOICES = (
    ('P', 'POP'),
    ('G', 'GOSPEL'),
    ('R', 'ROCK'),
    ('AP', 'AFRO POP'),
    ('RG', 'REGGAE'),
    ('H', 'HOUSE'),
    ('GN', 'GENERIC')
)


class Movie(models.Model):
    #slug = models.SlugField()
    title = models.CharField(max_length=250)
    film_type = models.CharField(choices=FILM_CHOICES, default='Home Entertainment', max_length=60)
    #position = models.IntegerField()
    details = models.TextField()
    movie = models.FileField(upload_to='videos/',validators=[video_validation_extention])#from validators.py
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])

    def get_absolute_url(self):
        return reverse('entertainments:movie.html')

    def __str__(self):
        return f"{self.title}, {self.movie}, {self.details},{self.cover_image}"

class Music(models.Model):
   # slug = models.SlugField()
    song_title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    music_genre = models.CharField(choices=SONG_CHOICES, default='GENERIC', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    song = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py

    def get_absolute_url(self):
        return reverse('entertainments:music')

    def __str__(self):
        return f"{self.song_title}, {self.artist}, {self.released_date}, {self.music_genre}, {self.cover_image},{self.song}"

class Podcast(models.Model):
    podcast_name = models.CharField(max_length=250)
    broadcaster = models.CharField(max_length=250)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    podcast_genre = models.CharField(choices=PODCAST_CHOICES , default='Other', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    upload_podcast = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py

    def get_absolute_url(self):
        return reverse('entertainments:podcast')

    def __str__(self):
        return f"{self.podcast_name}, {self.broadcaster}, {self.released_date}, {self.podcast_genre}, {self.cover_image}, {self.upload_podcast}"


class Comic(models.Model):
    #slug = models.SlugField()
    title = models.CharField(max_length=250)
    comedian = models.CharField(max_length=250)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    about_jokes = models.TextField()
    #commic_genre = models.CharField(choices=PODCAST_CHOICES , default='Other', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    upload_comedy = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py

    def get_absolute_url(self):
        return reverse('entertainments:comedy')
        
    def __str__(self):
        return f"{self.title}, {self.comedian}, {self.released_date}, {self.about_jokes}, {self.cover_image}, {self.upload_comedy}"

   