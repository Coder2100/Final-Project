from django.contrib import admin

# Register your models here.
from .models import BurnerSlide,TrendingAd,Story,Footer

admin.site.register(BurnerSlide)
admin.site.register(TrendingAd)
admin.site.register(Story)
admin.site.register(Footer)