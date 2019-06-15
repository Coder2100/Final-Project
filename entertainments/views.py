from django.shortcuts import render, get_object_or_404

from django.views.generic import CreateView
from django.views import generic

from .models import Comic, Music,Podcast, Movie, CommunityContent
from .forms import UploadForm

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

def community_content(request):
    context = {
        "community_contents": CommunityContent.objects.all()
    }

    return render(request, "entertainments/community.html", context)

class CreateFileView(CreateView):
    model = CommunityContent
    form_class = UploadForm
    template_name = 'entertainments/upload.html'
