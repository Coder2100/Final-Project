from django.urls import path
from django.conf.urls import url

from .views import (
    PlanSelectView,
    PaymentView,
    updateTransactionRecords,
    profile_view,
    cancelSubscription,
    add_to_cart,
    delete_from_cart,
    checkout,
    update_transaction_records,
    success,
    order_details,
    option_list
)


app_name = 'plans'

urlpatterns = [
    path('', PlanSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/',
         updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancelSubscription, name='cancel'),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', order_details, name="order_summary"),
    url(r'^success/$', success, name='purchase_success'),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart, name='delete_item'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', update_transaction_records,
        name='update_records'),
    url(r'^', option_list, name='option_list'),
    
]
