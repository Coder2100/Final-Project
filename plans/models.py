from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


PLAN_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)


class Plan(models.Model):
    slug = models.SlugField()
    plan_type=models.CharField(
        choices=PLAN_CHOICES,
        default='Free',
        max_length=30)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.plan_type


class UserPlan(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


def post_save_userplan_create(sender, instance, created, *args, **kwargs):
    user_plan, created = UserPlan.objects.get_or_create(
        user=instance)

    if user_plan.stripe_customer_id is None or user_plan.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        try:
            free_plan = Plan.objects.get(plan_type='Free')
        except Plan.DoesNotExist:
            free_plan = None
        user_plan.stripe_customer_id = new_customer_id['id']
        user_plan.plan = free_plan
        user_plan.save()


post_save.connect(post_save_userplan_create,
                  sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_plan = models.ForeignKey(
        UserPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_plan.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)
