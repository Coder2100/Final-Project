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
from . models import Profile
from plans.models import Plan, UserPlan, Subscription
from plans.views import (
    get_user_plan,
    get_user_subscription,
    get_selected_plan
)


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
@login_required(login_url='accounts:login')
def profile_view(request):
    user_plan = get_user_plan(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_plan': user_plan,
        'user_subscription': user_subscription
    }
 
    return render(request, "plans/profile.html", context)