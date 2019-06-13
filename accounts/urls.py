from django.urls import path

from django.conf.urls import url
from .views import profile, register, login_view, logout_view
app_name = 'accounts'

urlpatterns = [
    path("register",register, name="register"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    url(r'^profile/$', profile, name='profile'),
]
