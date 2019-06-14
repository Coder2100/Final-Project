from django.urls import path
from django.conf.urls import url

from .views import (
    add_to_cart,
    delete_from_cart,
    checkout,
    update_transaction_records,
    success,
    order_summary,
    option
)

from plans import views
app_name = 'plans'

urlpatterns = [
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    #url(r'^order_summary/$', order_details, name="order_summary"),
    path("order_summary", views.order_summary, name="order_summary"),
    url(r'^success/$', success, name='purchase_success'),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart, name='delete_item'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', update_transaction_records,
        name='update_records'),
    path("option", views.option, name="option")
    
]
