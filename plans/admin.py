from django.contrib import admin

# Register your models here.
from .models import Plan, UserPlan, Subscription ,Option

admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(Subscription)
admin.site.register(Option)