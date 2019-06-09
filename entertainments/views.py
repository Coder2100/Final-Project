from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from plans.models import UserPlan
from .models import Entertainment, Movie

# Create your views here.

#class based view
class EntertainmentListView(ListView):
    model = Entertainment

class EntertainmentDetailView(DetailView):
    model = Entertainment

class MovieDetailView(LoginRequiredMixin, View):
        def get(self, request, entertainment_slug, movie_slug, *args, **kwargs):
            entertainment = get_object_or_404(Entertainment, slug=entertainment_slug)
            movie = get_object_or_404(Movie, slug=movie_slug)
            user_plan = get_object_or_404(UserPlan, user=request.user)
            user_plan_type = user_plan.plan.plan_type
            entertainment_allowed_opt_types = entertainment.allowed_options.all()
            context = { 'object': None }
            if entertainment_allowed_opt_types.filter(plan_type=user_plan_type).exists():
                context = {'object': movie}
                return render(request, "entertainments/movie_detail.html", context)   
        
        
   
