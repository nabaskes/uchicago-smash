from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from uchicagosmash.powerranking import urls, views


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uchicagosmash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('uchicagosmash.powerranking.urls')),

)
