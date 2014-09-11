from django.shortcuts import render
from django.views.generic import DetailView
from uchicagosmash.powerranking.models import *


class PowerRankingView(DetailView):
	game = None
	template_name = 'power_ranking.html'

	def get_context_data(request, **kwargs):
		context = super(PowerRankingView, self).get_context_data(**kwargs)
		pr = []		
		smashers = Smasher.objects.all()
		for smasher in smashers:
			if game == "melee":
				d = {'smasher':smasher.tag, 'elo':smasher.melee_elo}
			elif game == "pm":
				d = {'smasher':smasher.tag, 'elo':smasher.pm_elo}
			elif game == "smash4":
				d = {'smasher':smasher.tag, 'elo':smasher.smash4_elo}
			pr.append(d)
		context['power_ranking'] = pr.sort(key=lambda x: x['elo'], reverse=True)	
		return context
			
