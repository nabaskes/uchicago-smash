from django.shortcuts import render
from django.views.generic import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from uchicagosmash.powerranking.models import *
from uchicagosmash.powerranking.forms import *
from uchicagosmash.powerranking.elo import calculate_elo

def login(request):
	return auth_views.login(request, 'login.html')

def logout(request):
	return auth_views.logout(request, '/')

class RegistrationView(FormView):
	form_class = RegistrationForm
	template_name = 'power_ranking/registration.html'
	
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

class MatchRecordView(FormView):
	form_class = MatchForm
	template_name = 'power_ranking/record_match.html'

	def dispatch(self, request, *args, **kwargs):
		return super(MatchRecordView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		match = form.save(commit=False)
		match.submitter = Smasher.objects.filter(user=self.request.user)[0]
		match.save()
		return HttpResponseRedirect('/')

class MatchVerificationView(UpdateView):
	model = Match
	form_class = MatchVerificationForm
	template_name = 'power_ranking/verify_match.html'

	def form_valid(self, form):
		match = form.save(commit=False)
		winner = match.winner
		loser = match.loser
		updated_elo = calculate_elo(winner.elo[match.game], loser.elo[match.game])
		winner.elo[match.game] = updated_elo[0]
		loser.elo[match.game] = updated_elo[1]
		winner.save()
		loser.save()
		match.save()
		return HttpResponseRedirect('/')

class MatchVerificationList(ListView):
	model = Match
	template_name = "power_ranking/unverified_matches.html"

	def get_context_data(self, **kwargs):
		context = super(MatchVerificationList, self).get_context_data(**kwargs)
		my_unverified_matches = Match.objects.filter(Q(winner__user=self.request.user) | Q(loser__user=self.request.user), verified=False)
		context['matches'] = my_unverified_matches
		context['smasher'] = Smasher.objects.filter(user=self.request.user)[0]
		return context

class PowerRankingView(ListView):
	model = Smasher
	game = None
	template_name = 'power_ranking/display.html'

	def get_context_data(self, **kwargs):
		context = super(PowerRankingView, self).get_context_data(**kwargs)
		pr = []		
		smashers = Smasher.objects.all()
		for smasher in smashers:
			d = {'smasher':smasher.tag, 'elo':smasher.elo[game]}
			pr.append(d)
		context['power_ranking'] = pr.sort(key=lambda x: x['elo'], reverse=True)	
		return context
			
