from django.conf import settings

from django.db import models

#from django.db.models.signals import post_save
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
    ('RS', 'Reality TV Show')
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
    ('GN', 'GERIC')
)

class Entertainment(models.Model):
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
    entertainment = models.ForeignKey(Entertainment, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=300)
    cover_image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entertainment:movie-detail',
                       kwargs={
                           'entertainment_slug': self.entertainment.slug,
                           'movie_slug': self.slug
                       })