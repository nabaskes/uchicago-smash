from django.contrib import admin
from django import forms
from uchicagosmash.powerranking.models import *


class SmasherAdmin(admin.ModelAdmin):
	form = forms.ModelForm
	list_filter = ('tag', 'dorm')
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'tag')


class MatchAdmin(admin.ModelAdmin):
	form = forms.ModelForm
	list_filter = ('winner', 'loser', 'verified')
	search_fields = ('winner__tag', 'loser__tag')

admin.site.register(Smasher, SmasherAdmin)
admin.site.register(Match, MatchAdmin)
