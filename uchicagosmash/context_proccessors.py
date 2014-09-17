from uchicagosmash.powerranking.models import *
from django.db.models import Q

def notification(request):
	unverified_matches = Match.objects.filter(Q(winner__user=request.user) | Q(loser__user=request.user), verified=False).count()
	return {'notifications':unverified_matches}
