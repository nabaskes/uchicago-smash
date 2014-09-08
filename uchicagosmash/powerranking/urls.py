from django.conf.urls import patterns, include, url
from uchicagosmash.powerranking.views import HomePage

urlpatterns = patterns('',
	url(r'^$', HomePage.as_view(), name='home'),

)
