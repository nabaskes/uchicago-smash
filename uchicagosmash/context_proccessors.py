from uchicagosmash.powerranking.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def notification(request):
	if request.user.is_authenticated():
		unverified_matches = Match.objects.filter(Q(winner__user=request.user) | Q(loser__user=request.user), verified=False).count()
		smasher = Smasher.objects.filter(user=request.user)
		if smasher:
			tag = smasher[0].tag
		else:
			tag = ''
	else:
		unverified_matches = 0
		tag = ''
	return {'notifications':unverified_matches, 'tag':tag}
