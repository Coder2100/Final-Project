from django.urls import path

#from .views import  EntertainmentListView, EntertainmentDetailView, MovieDetailView
from .views import EntertainmentListView, EntertainmentDetailView, MovieDetailView
    

app_name = 'entertainments'

urlpatterns = [
    path('', EntertainmentListView.as_view(), name='list'),
    path('<slug>', EntertainmentDetailView.as_view(), name='detail'),
    path('<entertainment_slug>/<movie_slug>', MovieDetailView.as_view(), name='movie-detail')
]
