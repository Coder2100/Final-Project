from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse

from .models import Plan, UserPlan, Subscription
import stripe
from accounts.models import Profile
from accounts.views import login_view, register
#from accounts.views import profile_view
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

@login_required(login_url='accounts:login')

def profile_view(request):
    user_plan = get_user_plan(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_plan': user_plan,
        'user_subscription': user_subscription
    }
 
    return render(request, "plans/profile.html", context)

class PlanSelectView(LoginRequiredMixin, ListView):
    model = Plan
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_plan = get_user_plan(self.required)
        context['current_plan'] = str(current_plan.plan)
        return context

    def post(self, request, **kwargs):
        user_plan = get_user_plan(request)
        user_subscription = get_user_subscription(request)
        selected_plan_type = request.POST.get('plan_type')

        selected_plan = Plan.objects.get(plan_type=selected_plan_type)

        if user_plan.plan == selected_plan:
            if user_subscription is not None:
                messages.info(request, """ This is your current Plan option. Your next payment date {} """.format('get this value from stipe'))
                return HttpResponseRedirect(request,META.get('HTTP_REFERER'))

            request.session['selected_plan_type'] = selected_type.plan_type
            return HttpResponseRedirect(reverse('plans:payment'))

def PaymentView(request):
    user_plan = get_user_plan(request)
    try:
        selected_plan = get_selected_plan(request)
    except:
        return redict(reverse("plans:select"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            customer = stripe.Customer.retrieve(user_plan.stripe_customer_id)
            customer.source = token
            customer.save()

            subscription = stripe.Subscription.create(
                customer=user_plan.stripe_customer_id,
                items = [
                    {"option": selected_plan.stripe_plan_id},
                ])
            return redirect(reverse('plan:update-transactions',kwargs={'subscription_id':subscription.id}))
        except:
            messages.info(request, "Something went wrong, check the issue on your browser's dev tools")
    context = {
        'publishKey': publishKey,
        'selected_plan':selected_plan
    }

    return render(request, "plans/payment.html", context)

@login_required(login_url='accounts:login')
def updateTransactionRecords(request, subscription_id):
    user_plan = get_user_plan(request)
    selected_plan = get_selected_plan(request)
    user_plan.plan = selected_plan
    user_plan.save()

    sub, created = Subscription.objects.get_or_create(
        user_plan=user_plan)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_plan_type']
    except:
        pass

    messages.info(request, 'Successfully created {} plan'.format(
        selected_plan))
    return redirect(reverse('plans:select'))

@login_required(login_url='accounts:login')
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active Plan option")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_plan = Plan.objects.get(plan_type='Free')
    user_plan = get_user_plan(request)
    user_plan.plan = free_plan
    user_plan.save()

    messages.info(
        request, "Successfully cancelled . We have sent an email")
    # to add email confirmation later

    return redirect(reverse('s:select'))

            


