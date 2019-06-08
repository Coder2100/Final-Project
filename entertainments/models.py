from django.conf import settings

from django.db import models

from django.db.models.signals import post_save
from datetime import datetime

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
