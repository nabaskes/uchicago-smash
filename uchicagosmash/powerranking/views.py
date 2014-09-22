from django.shortcuts import render
from django.views.generic import *
from django.views.generic.base import TemplateView
from django.shortcuts import *
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

class HomeView(TemplateView):
	template_name = "index.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated() and not Smasher.objects.filter(user=request.user).exists():
			return redirect("register-smasher")
		return super(HomeView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		smashers = Smasher.objects.all()
		context['top_melee'] = smashers.order_by('-melee')[:5]
		context['top_pm'] = smashers.order_by('-pm')[:5]
		context['top_smash4'] = smashers.order_by('-smash4')[:5]
		return context

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
		match.submitter = get_object_or_404(Smasher, user= self.request.user)
		match.save()
		return HttpResponseRedirect('/')

class VerifyMatch(DetailView):
	model = Match
	template_name = 'power_ranking/verify_match.html'

	def dispatch(self, *args, **kwargs):
		match = get_object_or_404(Match, id=self.kwargs['pk'])
		match.verified = True
		match.save()
		return redirect("unverified-matches")

class DeleteMatch(DetailView):
	model = Match
	template_name = 'power_ranking/delete_match.html'

	def dispatch(self, *args, **kwargs):
		match = get_object_or_404(Match, id=self.kwargs['pk'])
		match.delete()
		return redirect("unverified-matches")

class MatchVerificationList(ListView):
	model = Match
	template_name = "power_ranking/unverified_matches.html"

	def get_context_data(self, **kwargs):
		context = super(MatchVerificationList, self).get_context_data(**kwargs)
		my_unverified_matches = Match.objects.exclude(submitter__user=self.request.user).filter(Q(winner__user=self.request.user) | Q(loser__user=self.request.user), verified=False)
		context['matches'] = my_unverified_matches
		context['smasher'] = Smasher.objects.filter(user=self.request.user)[0]
		return context

class PowerRankingView(ListView):
	model = Smasher
	game = None
	template_name = 'power_ranking/display.html'

	def get_context_data(self, **kwargs):
		context = super(PowerRankingView, self).get_context_data(**kwargs)	
		smashers = Smasher.objects.all()
		if self.game == "melee":
			pr = smashers.order_by('-melee')
		elif self.game == "pm":
			pr = smashers.order_by('-pm')
		elif self.game == "smash4":
			pr = smashers.order_by('-smash4')
		context['power_ranking'] = pr
		context['game'] = self.game
		return context
			
