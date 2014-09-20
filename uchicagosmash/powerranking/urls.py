from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from uchicagosmash.powerranking.views import *

urlpatterns = patterns('',
	url(r'^$', HomeView.as_view(), name='home'),
	url(r'^power_ranking/melee/$', PowerRankingView.as_view(game="melee"), name='pr-melee'),
	url(r'^power_ranking/pm/$', PowerRankingView.as_view(game="pm"), name='pr-pm'),
	url(r'^power_ranking/smash4/$', PowerRankingView.as_view(game="smash4"), name='pr-smash4'),
	url(r'^record_match/$', MatchRecordView.as_view(), name='record-match'),
	url(r'^verify_match/(?P<pk>[0-9]+)/$', VerifyMatch.as_view(), name='verify-match'),
	url(r'^delete_match/(?P<pk>[0-9]+)/$', DeleteMatch.as_view(), name='delete-match'),
	url(r'^unverified_matches/$', MatchVerificationList.as_view(), name='unverified-matches'),
	url(r'^register/$', RegistrationView.as_view(), name='register-smasher'),
	url(r'^login/$', login, name='login'),
	url(r'^logout/$', logout, name='logout'),
)
