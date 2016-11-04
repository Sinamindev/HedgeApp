from django.db import models


class Portfolio(models.Model):
	username = models.CharField(max_length=80, primary_key=True)
	money = models.DecimalField(max_digits=20, decimal_places=2)
	add_date = models.DateTimeField('Date added')

	def __str__(self):
		return self.username


class Transaction(models.Model):
	user = models.ForeignKey(Portfolio)
	symbol = models.CharField(max_length=8)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=20, decimal_places=2)
	date = models.DateTimeField('Date added')
	buy = models.BooleanField()

	def __str__(self):
		uname = self.user.username
		tr_type = 'Sell'
		if self.buy:
			tr_type = 'Buy'
		q = self.quantity
		s = self.symbol
		label = "{} - {} {} {}".format(uname, tr_type, q, s)
		return label


class Owned(models.Model):
	user = models.ForeignKey(Portfolio)
	symbol = models.CharField(max_length=8)
	quantity = models.IntegerField()
	avg_price = models.DecimalField(max_digits=20, decimal_places=2)

	def __str__(self):
		uname = self.user.username
		s = self.symbol
		q = self.quantity
		label = "{} - {} {}".format(uname, s, q)
		return label


class Watchlist(models.Model):
	user = models.ForeignKey(Portfolio)
	symbol = models.CharField(max_length=8)
	company = models.CharField(max_length=40)

	def __str__(self):
		uname = self.user.username
		s = self.symbol
		label = "{} - {}".format(uname, s)
		return label

