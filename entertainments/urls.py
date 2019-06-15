from django.urls import path, include

from entertainments import views
from .views import CreateFileView
    
app_name = 'entertainments'

urlpatterns = [  
     path("comic", views.comic, name="comic"),
     path("movie", views.movie, name="movie"),
     path("music", views.music, name="music"),
     path("podcast", views.podcast, name="podcast"),
     path("community", views.community_content, name="community"),
     path('upload/', CreateFileView.as_view(), name='upload'),
]
