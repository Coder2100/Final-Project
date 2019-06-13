from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse

from .models import Plan, UserPlan, Subscription, Option
import stripe
from accounts.models import Profile
from accounts.views import login_view, register
from plans.helpers import generate_order_id

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
        current_plan = get_user_plan(self.request)
        context['current_plan'] = str(current_plan.plan)
        return context

    def post(self, request, **kwargs):
        user_plan = get_user_plan(request)
        user_subscription = get_user_subscription(request)
        selected_plan_type = request.POST.get('plan_type')

        selected_plan = Plan.objects.get(
            plan_type=selected_plan_type)

        if user_plan.plan == selected_plan:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                              next payment is due {}""".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_plan_type'] = selected_plan.plan_type

        return HttpResponseRedirect(reverse('plans:payment'))

def PaymentView(request):
    user_plan = get_user_plan(request)
    try:
        selected_plan = get_selected_plan(request)
    except:
        return redirect(reverse("plans:select"))
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

    #list of options
def option_list(request):
    option = Option.objects.all()
    filtered_ordered = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_ordered_options = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_options = [option.option for option in user_order_items]

        context = {
            'options': option,
            'profiles':Profile.objects.all()
           # 'options': Option.objects.all()
        }
    return render(request, "plans/plan_list.html", context)

def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0

def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    option = Option.objects.filter(id=kwargs.get('item', "")).first()
    #check if the user currently has the option
    if option in request.user.profile.istream_plans.all():
        message.info(request, 'This is your current plan')
        return redirect(reverse('plans:plan_list'))

        #create order for the selected plan
    order_item, status =  OrderItem.objects.get_or_create(option=option)



    #associate the option with the user
    user_order.items.add(oder_item)
    if status:
        #generate order rfere code
        user_order.ref_code = generate_order_id()
        user_order.save()
    messages.info(request, "item added to the cart")
    return redirect(reverse('plans:plan_list'))

def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item-to_delete.exits():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('plans:order_summary'))


def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'plans/order_summary', context)

def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return redirect(reverse('plans:update_records',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('plans:update_records',
                        kwargs={
                            'token': result.transaction.id
                        })
                    )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('plans:checkout'))

    context = {
        'order': existing_order,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'plans/checkout.html', context)


def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()

    # get all options in the order - generates a queryset which is one
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_options = [item.option for item in order_items]
    user_profile.istream_options .add(*order_options)
    user_profile.save()


    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # proof of transaction that it was successful
    return render(request, 'plans/purchase_success.html', {})


