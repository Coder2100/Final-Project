
from django.conf import settings
from django.contrib import admin
from django.urls import  include, path
from django.conf.urls import url, include
# import for media files

from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("ads.urls")),
    path("", include("accounts.urls")),
    url(r'^entertainments', include('entertainments.urls')),
  #path('entertainments/', include('entertainments.urls', namespace='entertainments')),
   # path('plans/', include('plans.urls', namespace='plans')),
    url(r'^plans/', include('plans.urls', namespace='options')),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

