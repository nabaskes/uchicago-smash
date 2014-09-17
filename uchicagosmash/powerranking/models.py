from django.db import models
from django.conf import settings


DORMS = (
	("BS", "Blackstone"),
	("BR", "Breckinridge"),
	("BV", "Broadview"),
	("BJ", "Burton-Judson Courts"),
	("IH", "International House"),
	("MC", "Maclean"),
	("MAX", "Max Palevsky"),
	("NG", "New Graduate Residence Hall"),
	("SH", "Snell-Hitchcock"),
	("SC", "South Campus"),
	("ST", "Stony Island"),
	("OFF", "Off campus")
)

GAMES = (
	("M", "Super Smash Bros Melee"),
	("P:M", "Project M"),
	("S4", "Smash Bros for Wii U/3DS"),
)

class Smasher(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
	tag = models.CharField(max_length=64)	
	dorm = models.CharField(max_length=4, choices=DORMS)
	melee_elo = models.IntegerField(default=0)
	pm_elo = models.IntegerField(default=0)
	smash4_elo = models.IntegerField(default=0)

class Match(models.Model):
	winner = models.ForeignKey(Smasher, related_name="winners")
	loser = models.ForeignKey(Smasher, related_name="losers")
	players = [winner, loser]
	game = models.CharField(max_length=4, choices=GAMES)
	verified = models.BooleanField(default=False)
