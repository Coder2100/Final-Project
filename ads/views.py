from django.shortcuts import render

from .models import*
# Create your views here.

def index(request):
    context ={ 
        "footers":Footer.objects.all(),
        "BurnerSlides": BurnerSlide.objects.all(),
        "trendingAds":TrendingAd.objects.all(),
        "stories":Story.objects.all()
    }
    return render(request, 'ads/index.html', context)