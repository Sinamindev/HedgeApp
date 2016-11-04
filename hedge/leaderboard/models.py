
from django.db import models
from portfolio.models import Portfolio


class Valuation(models.Model):
	user = models.ForeignKey(Portfolio)
	current_valuation = models.DecimalField(max_digits=20, decimal_places=2)
	day_valuation = models.DecimalField(max_digits=20, decimal_places=2)
	week_valuation = models.DecimalField(max_digits=20, decimal_places=2)
	month_valuation = models.DecimalField(max_digits=20, decimal_places=2)
	year_valuation = models.DecimalField(max_digits=20, decimal_places=2)

	def __str__(self):
		return "{0}'s valuations".format(self.user.username)
