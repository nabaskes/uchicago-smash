from uchicagosmash.powerranking.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def notification(request):
	if request.user.is_authenticated():
		unverified_matches = Match.objects.filter(Q(winner__user=request.user) | Q(loser__user=request.user), verified=False).exclude(submitter__user=request.user).count()
		query = Smasher.objects.filter(user=request.user)
		if query:
			tag = query[0].tag
			smasher = query[0]
		else:
			smasher = None
			tag = ''
	else:
		unverified_matches = 0
		tag = ''
		smasher = None
	return {'notifications':unverified_matches, 'tag':tag, 'smasher':smasher}
