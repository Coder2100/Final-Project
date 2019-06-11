from django.urls import path, include

#from .views import  EntertainmentListView, EntertainmentDetailView, MovieDetailView
from .views import*  #EntertainmentListView, EntertainmentDetailView, MovieDetailView
    

app_name = 'entertainments'

urlpatterns = [
    path('', EntertainmentListView.as_view(), name='list'),
    path('<slug>', EntertainmentDetailView.as_view(), name='detail'),
    path('<entertainment_slug>/<movie_slug>', MovieDetailView.as_view(), name='movie-detail'),
    path('entertainment_list/',MusicView.as_view(), name='music' ),
    path('entertainment_list/',PodcastView.as_view(), name='podcast' ),
    path('entertainment_list/',ComedyView.as_view(), name='commedy' ),  
]
