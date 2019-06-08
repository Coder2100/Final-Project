from django.urls import path

from accounts.views import profile_view

app_name = 'plans'

urlpatterns = [
path('profile/', profile_view, name='profile'),
]
