from django.urls import path

from .views import (
    PlanSelectView,
    PaymentView,
    updateTransactionRecords,
    profile_view,
    cancelSubscription
)

app_name = 'plans'

urlpatterns = [
    path('', PlanSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/',
         updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancelSubscription, name='cancel')
]
