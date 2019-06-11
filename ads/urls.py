from django.urls import path
#from django.conf.urls import url
from .views import index



app_name = 'ads'
urlpatterns = [
    path("", index, name="index"),
]