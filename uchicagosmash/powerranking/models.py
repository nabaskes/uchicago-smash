from django.db import models
from django.conf import settings
from django.utils import timezone
from uchicagosmash.powerranking.elo import calculate_elo


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
	melee = models.IntegerField(default=1000)
	pm = models.IntegerField(default=1000)
	smash4 = models.IntegerField(default=1000)

	def get_real_name(self):
		return self.user.get_full_name()

	def __unicode__(self):
		name = self.user.get_full_name()
		return "%s, %s" % (self.tag, name)

class Match(models.Model):
	winner = models.ForeignKey(Smasher, related_name="winners")
	loser = models.ForeignKey(Smasher, related_name="losers")
	game = models.CharField(max_length=8, choices=GAMES)
	date = models.DateTimeField(default=timezone.now)
	verified = models.BooleanField(default=False)
	submitter = models.ForeignKey(Smasher, related_name="submitters")

	def __unicode__(self):
		return "%s; Winner: %s Loser: %s" % (self.game, self.winner.tag, self.loser.tag)

	def save(self):
		if self.verified:
			if self.game == 'melee':
				updated_elo = calculate_elo(self.winner.melee, self.loser.melee)
				self.winner.melee = updated_elo[0]
				self.loser.melee = updated_elo[1]
				self.winner.save()
				self.loser.save()
			elif self.game == 'pm':
				updated_elo = calculate_elo(self.winner.pm, self.loser.pm)
				self.winner.pm = updated_elo[0]
				self.loser.pm = updated_elo[1]
				self.winner.save()
				self.loser.save()
			elif self.game == 'smash4':
				updated_elo = calculate_elo(self.winner.smash4, self.loser.smash4)
				self.winner.smash4 = updated_elo[0]
				self.loser.smash4 = updated_elo[1]
				self.winner.save()
				self.loser.save()
		super(Match, self).save()
