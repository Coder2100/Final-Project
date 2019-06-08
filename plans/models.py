from django.conf import settings
from django.db import models

from django.db.models.signals import post_save
from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
PLAN_CHOICES = (
    ('Enterprise', 'Enterpise'),
    ('Professional', 'Professional'),
    ('Free', 'Free')
)

class Plan(models.Model):
    slug = models.SlugField()
    plan_type = models.CharField(
        choices=PLAN_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.plan_type

        return self.user.username

class UserPlan(models.Model):
    user = user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}"
def post_saveuserplan_create(sender, instance, created, *args, **kwargs):
    user_plan, creted = UserPlan.objects.get_or_create(user=instance)
#logic to default membership to free if the user has not subscribed to any plan
    if user_plan.stripe_customer_id is None or user_plan.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        free_plan = Plan.objects.get(plan_type='Free')
        user_plan.stripe_customer_id = new_custmer_id['id']
        user_plan.plan = free_plan
        user_plan.save()
post_save.connect(post_saveuserplan_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_plan.user.username}"
@property
def get_created_date(self):
    subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
    return datetime.fromtimestamp(subscription.created)

@property
def get_next_billing_date(self):
    subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
    return datetime.fromtimestamp(subscription.current_period_end)


    
