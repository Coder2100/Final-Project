from django.urls import path

from accounts import views
#from django.conf.urls import url
from .views import register, login_view, logout_view
app_name = 'accounts'

urlpatterns = [
    path("register",register, name="register"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
]
