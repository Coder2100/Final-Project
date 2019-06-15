from django.shortcuts import render

from .models import*
from entertainments.models import CommunityContent
#from random import shuffle
# Create your views here.

def index(request):
    
    context ={ 
        "footers":Footer.objects.all(),
       # "BurnerSlides": BurnerSlide.objects.all(),
        "trendingAds":TrendingAd.objects.all(),
        "community_contents":CommunityContent.objects.all().order_by('-id')[:4]
       # "stories":Story.objects.all()
    }
    return render(request, 'ads/index.html', context)

def ads(request):
    context ={ 
        #"footers":Footer.objects.all(),
        "BurnerSlides": BurnerSlide.objects.all(),
        #"trendingAds":TrendingAd.objects.all(),
        #"stories":Story.objects.all()
    }
    return render(request, 'entertainments/community.html', context)