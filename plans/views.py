from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse

from .models import Plan, UserPlan, Subscription
import stripe

# Create your views here.

def get_user_plan(request):
    user_plan_querySet = UserPlan.objects.filter(user=request.user)
    if user_plan_querySet.exists():
        return user_plan_querySet.first()
    return None

def get_user_subscription(request):
    user_subscription_querySet = Subscription.objects.filter(user_plan=get_user_plan(request))

    if user_subscription_querySet.exists():
        user_subscription = user_subscription_querySet.first()
        return user_subscription
    return None

def get_selected_plan(request):
    plan_type = request.session['selected_plan_type']
    selected_plan_querySet = Plan.objects.filter(plan_type=plan_type)
    if selected_plan_querySet.exists():
        return selected_plan_querySet.first()
    return None

    # required auth
"""
def profile_view(request):
    user_plan = get_user_plan(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_plan': user_plan,
        'user_subscription': user_subscription
    }
    return render(request, "plans/profile.html", context)
    """


