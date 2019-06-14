from django.urls import path, include
from django.conf.urls import url

from .views import* 
from entertainments import views
    
app_name = 'entertainments'

urlpatterns = [
    path('entertainment_list/',MusicView.as_view(), name='music' ),
    path('entertainment_list/',PodcastView.as_view(), name='podcast' ),
    #path('entertainment_list/',ComedyView.as_view(), name='commedy' ),
    url(r'^$', views.HomeView.as_view(),name='home' ),  
    path("comic", views.comic, name="comic")
]
