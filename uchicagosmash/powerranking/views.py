from django.shortcuts import render
from django.views.generic import DetailView

class PowerRankingView(DetailView):
	game = None
	template_name = 'power_ranking.html'

	def get_context_data(request, **kwargs):
		context = super(PowerRankingView, self).get_context)data(**kwargs)	
		return context
			
