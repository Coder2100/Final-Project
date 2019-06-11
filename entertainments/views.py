from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from plans.models import UserPlan
from .models import *

# Create your views here.

#class based view
class EntertainmentListView(ListView):
    model = EntertainmentOption
   
def EntertainmentList(request):
    context = {
        #"entertainments":Entertainment.objects.all() 
        "entertainments": EntertainmentOption.objects.all()
    }
    return render(request, "entertainments/entertainment_list", context)

class EntertainmentDetailView(DetailView):
    model = EntertainmentOption

class MovieDetailView(LoginRequiredMixin, View):
        def get(self, request, entertainment_slug, movie_slug, *args, **kwargs):
            entertainment_option = get_object_or_404(EntertainmentOption, slug=entertainment_slug)
            movie = get_object_or_404(Movie, slug=movie_slug)
            user_plan = get_object_or_404(UserPlan, user=request.user)
            user_plan_type = user_plan.plan.plan_type
            entertainment_allowed_opt_types = entertainment_option.allowed_options.all()
            context = { 'object': None }
            if entertainment_allowed_opt_types.filter(plan_type=user_plan_type).exists():
                context = {'object': movie}
                return render(request, "entertainments/movie_detail.html", context)   
        
        
class MusicView(ListView):
    model = Music
    template_name = 'entertainments/entertainment_list'    # this is temporary since details will be displayed separate

class PodcastView(ListView):
    model = Podcast
    template_name = 'entertainments/entertainment_list'

class ComedyView(ListView):
    model = Comedy
    template_name = 'entertainments/entertainment_list'
    

