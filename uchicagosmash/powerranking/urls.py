from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from uchicagosmash.powerranking.views import Leaderboard

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
	url(r'^power_ranking/melee/$', Leaderboard(game="melee"), name='melee_pr'),
)
