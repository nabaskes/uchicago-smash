from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from uchicagosmash.powerranking.views import *

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
	url(r'^power_ranking/melee/$', PowerRankingView.as_view(game="melee"), name='pr-melee'),
	url(r'^power_ranking/pm/$', PowerRankingView.as_view(game="pm"), name='pr-pm'),
	url(r'^power_ranking/smash4/$', PowerRankingView.as_view(game="smash4"), name='pr-smash4'),
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, name='logout'),
)
