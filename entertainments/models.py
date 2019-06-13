from django.conf import settings

from django.db import models
from django.urls import reverse
#from django.core.validators import FileExtensionValidator
from .validators import image_validation_extension,video_validation_extention

from datetime import datetime
from plans.models import Plan

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your models here.

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

class EntertainmentOption(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_plans = models.ManyToManyField(Plan)


    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('entertainments:detail', kwargs={'slug': self.slug})

    @property
    def movies(self):
        return self.movie_set.all().order_by('position')


class Movie(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    entertainmentOption = models.ForeignKey(EntertainmentOption, on_delete=models.SET_NULL, null=True)
    film_type = models.CharField(choices=FILM_CHOICES, default='Home Entertainment', max_length=60)
    position = models.IntegerField()
    details = models.TextField()
    movie = models.FileField(upload_to='videos/',validators=[video_validation_extention])#from validators.py
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])

    def __str__(self):
        return f"{self.title}, {self.movie}, {self.details}, {self.film_type}, {self.cover_image}, {self.entertainmentOption}"

    def get_absolute_url(self):
        return reverse('entertainments:movie-detail',
                       kwargs={
                           'entertainmentOption_slug': self.entertainmentOption.slug,
                           'movie_slug': self.slug
                       })


class Music(models.Model):
    slug = models.SlugField()
    song_name = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    entertainmentOption = models.ForeignKey(EntertainmentOption, on_delete=models.SET_NULL, null=True)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    music_genre = models.CharField(choices=SONG_CHOICES, default='GENERIC', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    song = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py

    def __str__(self):
        return f"{self.song_name}, {self.artist}, {self.released_date}, {self.music_genre}, {self.cover_image}, {self.entertainmentOption}, {self.song}"

    def get_absolute_url(self):
        return reverse('entertainments:song-detail',
                       kwargs={
                           'entertainmentOption_slug': self.entertainmentOption.slug,
                           'song_slug': self.slug
                       })

class Podcast(models.Model):
    slug = models.SlugField()
    song_name = models.CharField(max_length=250)
    broadcaster = models.CharField(max_length=250)
    entertainmentOption = models.ForeignKey(EntertainmentOption, on_delete=models.SET_NULL, null=True)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    podcast_genre = models.CharField(choices=PODCAST_CHOICES , default='Other', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    upload_podcast = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py


    def __str__(self):
        return f"{self.song_name}, {self.artist}, {self.released_date}, {self.podcast_genre}, {self.cover_image}, {self.entertainmentOption}, {self.song}, {self.distribution_rights}"

    def get_absolute_url(self):
        return reverse('entertainments:podcast-detail',
                       kwargs={
                           'entertainmentOption_slug': self.entertainmentOption.slug,
                           'podcast_slug': self.slug
                       })

class Comedy(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=250)
    comedian = models.CharField(max_length=250)
    entertainmentOption = models.ForeignKey(EntertainmentOption, on_delete=models.SET_NULL, null=True)
    released_date = models.DateField()
    distribution_rights = models.TextField()
    about_jokes = models.TextField()
    commic_genre = models.CharField(choices=PODCAST_CHOICES , default='Other', max_length=60)
    cover_image = models.ImageField(upload_to='images/',validators=[image_validation_extension])
    upload_comedy = models.FileField(upload_to='audios/',validators=[video_validation_extention])#from validators.py


    def __str__(self):
        return f"{self.song_title}, {self.comedian}, {self.released_date}, {self.about_jokes}, {self.cover_image}, {self.entertainmentOption}, {self.upload_comedy}"

    def get_absolute_url(self):
        return reverse('entertainments:podcast-detail',
                       kwargs={
                           'entertainmentOption_slug': self.entertainmentOption.slug,
                           'comedy_slug': self.slug
                       })
