from django.test import TestCase
from .models import Valuation
from portfolio.models import Portfolio
from django.utils.timezone import now
from datetime import datetime
from decimal import Decimal
try:
	from django.utils.timezone import now as datetime_now
except ImportError:
	datetime_now = datetime.datetime.now

# Create your tests here.
class ValuationTestCase(TestCase):
    def setUp(self):
        #create portfolio object
        p = Portfolio(username = "usr", money = 1.0, add_date = now())
        d = Decimal(1234000.56)
        Valuation.objects.create(user=p, current_valuation=d,
        day_valuation = d, week_valuation = d,
        month_valuation = d, year_valuation = d)

    def test_Valuation(self):
        usr = Valuation.objects.get(user="usr")
        self.assertNotEqual(usr, None)
        self.assertEqual(usr.current_valuation, round(Decimal(1234000.56),2))
