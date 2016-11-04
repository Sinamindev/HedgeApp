from django.test import TestCase
#test
from .models import Portfolio, Transaction, Owned, Watchlist
from django.utils.timezone import now
from datetime import datetime

# Create your tests here.
#from django.db import models

try:
	from django.utils.timezone import now as datetime_now
except ImportError:
	datetime_now = datetime.datetime.now

class PortfolioTestCase(TestCase):
	def setUp(self):
		Portfolio.objects.create(username = "usr", money = 1.0, add_date = now())
		Portfolio.objects.create(username = "usr2", money = 123456789.0, add_date = now())
	#This shouldn't be necessary, but can't hurt...
	def test_Portfolio(self):
		usr = Portfolio.objects.get(username = "usr")
		usr2 = Portfolio.objects.get(username = "usr2")
		self.assertEqual(usr.money, 1.0)
		self.assertEqual(usr2.money, 123456789.0)


class TransactionTestCase(TestCase):
	def setUp(self):
		p = Portfolio(username = "usr", money = 1.0, add_date = now())
		Transaction.objects.create(user = p, symbol = "a", quantity = 1, price = 1.1, date = now(), buy = True)

	def test_Transaction(self):
		usr = Transaction.objects.get(user = "usr")
		self.assertEqual(usr.symbol, "a")


class OwnedCase(TestCase):
	def setUp(self):
		p = Portfolio(username = "usr", money = 1.0, add_date = now())
		Owned.objects.create(user = p, symbol = "a", quantity = 1, avg_price = 2.00)

	def test_Owned(self):
		usr = Owned.objects.get(user = "usr")
		self.assertEqual(usr.symbol, "a")


class WatchlistCase(TestCase):
	def setUp(self):
		p = Portfolio(username = "usr", money = 1.00, add_date = now())
		Watchlist.objects.create(user = p, symbol = "a", company = "google")

	def test_Owned(self):
		usr = Watchlist.objects.get(user = "usr")
		self.assertEqual(usr.symbol, "a")





