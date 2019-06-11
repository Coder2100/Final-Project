from django.contrib import admin
from .models import* # EntertainmentOption, Movie
# Register your models here.

admin.site.register(EntertainmentOption)
admin.site.register( Movie)
admin.site.register( Comedy)
admin.site.register( Music)
admin.site.register( Podcast)
