from django.urls import path, include

from entertainments import views
    
app_name = 'entertainments'

urlpatterns = [  
     path("comic", views.comic, name="comic"),
     path("movie", views.movie, name="movie"),
     path("music", views.music, name="music"),
     path("podcast", views.podcast, name="podcast"),
]
