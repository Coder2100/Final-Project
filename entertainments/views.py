from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views import generic
#from .models import *
from .models import Comic, Music,Podcast, Movie

def comic(request):
    context = {
        "comics": Comic.objects.all()
    }
    return render(request, "entertainments/comedy.html", context)

def movie(request):
    context = {
        "movies": Movie.objects.all()
    }
    return render(request, "entertainments/movie.html", context)

def podcast(request):
    context = {
        "podcasts": Podcast.objects.all()
    }
    return render(request, "entertainments/podcast.html", context)

def music(request):
    context = {
        "musics": Music.objects.all()
    }
    return render(request, "entertainments/music.html", context)