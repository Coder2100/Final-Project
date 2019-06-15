from django.contrib import admin
from .models import* 

admin.site.register( Movie)
admin.site.register( Comic)
admin.site.register( Music)
admin.site.register( Podcast)
admin.site.register(CommunityContent)
