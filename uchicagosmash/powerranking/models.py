from django.db import models


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

class Smasher(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
	tag = models.CharField(max_length=64)	
	dorm = models.CharField(max_length=4, choices=DORMS)
	melee_elo = models.IntegerField()
	pm_elo = models.IntegerField()
	smash4_elo = models.IntegerField()
