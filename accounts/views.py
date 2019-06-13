from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from .forms import MyUserLoginForm, MyUserRegistrationForm
from .models import Profile

# Create your views here.


def login_view(request):
    next = request.GET.get('next')
    form = MyUserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('ads:index')
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if not request.user.is_authenticated:
        next = request.GET.get('next')
        form = MyUserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email1')
            user.set_password(password)
            user.email = email
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('ads:index')
        return render(request, 'accounts/register.html', {'form': form})
    else:
        return redirect('ads:index')


@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('ads:index')


def profile(request):
    context ={
        'profiles': Profile.objects.all()
    }

    return render(request, "accounts/my_profile.html", context)