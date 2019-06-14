from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views import generic
from .models import *
from .models import Comic

class MusicView(ListView):
    model = Music
    template_name = 'entertainments/entertainment_list'    # this is temporary since details will be displayed separate

class PodcastView(ListView):
    model = Podcast
    template_name = 'entertainments/entertainment_list'

#class ComedyView(ListView):
   # model = Comedy
    #template_name = 'entertainments/entertainment_list'
    

class HomeView(generic.ListView):
    context_object_name = 'entertainment_list'
    template_name = 'entertainments/entertainment_list.html'
    #custom views

def comic(request):
    context = {
        "comics": Comic.objects.all()
    }
    return render(request, "entertainments/comedy.html", context)