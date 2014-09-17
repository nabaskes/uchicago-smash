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
	("melee", "Melee"),
	("pm", "Project M"),
	("smash4", "Smash Bros for Wii U/3DS"),
)

class Smasher(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
	tag = models.CharField(max_length=64)	
	dorm = models.CharField(max_length=4, choices=DORMS)
	elo = {}
	elo['melee'] = models.IntegerField(default=0)
	elo['pm'] = models.IntegerField(default=0)
	elo['smash4'] = models.IntegerField(default=0)

	def __unicode__(self):
		name = self.user.get_full_name()
		return "%s, %s, %s" % (self.tag, self.user.username, name)

class Match(models.Model):
	winner = models.ForeignKey(Smasher, related_name="winners")
	loser = models.ForeignKey(Smasher, related_name="losers")
	game = models.CharField(max_length=4, choices=GAMES)
	verified = models.BooleanField(default=False)

	def __unicode__(self):
		
		return "%s; Winner: %s Loser: %s" % (self.game, self.winner.tag, self.loser.tag)
