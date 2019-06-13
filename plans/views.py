from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse

from .models import Option
import stripe
from accounts.models import Profile
from accounts.views import login_view, register
from plans.helpers import generate_order_id


def option(request):
    context = {
         'options': Option.objects.all()
     }
    return render(request, "plans/option.html", context)

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


