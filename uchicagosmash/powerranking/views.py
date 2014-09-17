from django.shortcuts import render
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from uchicagosmash.powerranking.models import *
from uchicagosmash.powerranking.forms import *

def login(request):
	return auth_views.login(request, 'login.html')

def logout(request):
	return auth_views.logout(request, '/')

class RegistrationView(FormView):
	form_class = RegistrationForm
	template_name = 'power_ranking/registration.html'
	
	@login_required
	def dispatch(self, request, *args, **kwargs):
		if Smasher.objects.filter(user=request.user).exists():
			messages.error(self.request, "You are already registered.")
			return HttpResponseRedirect('/')
		return super(RegistrationView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		smasher = form.save(commit=False)
		smasher.user = self.request.user
		smasher.save()
		return HttpResponseRedirect('/')

class MatchReportView(FormView):
	form_class = MatchForm
	template_name = 'power_ranking/match_report.html'

	@login_required
	def dispatch(self, request, *args, **kwargs):
		return super(MatchReportView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		match = form.save(commit=False)
		match.save()
		return HttpResponseRedirect('/')

class PowerRankingView(DetailView):
	model = Smasher
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
			
