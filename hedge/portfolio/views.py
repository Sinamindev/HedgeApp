
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from registration.backends.default.views import ActivationView
from .models import Portfolio, Transaction, Owned, Watchlist
from leaderboard.models import Valuation
from .utils import get_valuation, unwatch, hash_user
from leaderboard.models import Valuation
from common.utils import get_price, get_prices, get_ticker_symbols

try:
	from django.utils.timezone import now as datetime_now
except ImportError:
	datetime_now = datetime.datetime.now

#TODO: wrap database .get calls in try, except DoesNotExist/getObjectOr404

def deactivate(request, user_key):
	username = request.user.username
	if user_key and user_key == hash_user(username):
		u = User.objects.get(username=username)
		u.is_active = False
		u.save()
		logout(request)
		update_session_auth_hash(request, request.user)
		return HttpResponseRedirect('/')
	else:
		msg = 'It appears you are attempting to deactivate your account. Try the "Account" button at the top of the page.'
		base_view(request, msg)


def reset_portfolio(request, user_key):
	username = request.user.username
	if user_key and user_key == hash_user(username):
		p = Portfolio.objects.get(username=username)
		d = Decimal(1000000.00)
		p.money = d
		p.save()
		for table in [Transaction, Owned, Watchlist]:
			table.objects.filter(user=p).delete()
		v = Valuation.objects.get(user=p)
		v.current_valuation = d
		v.day_valuation = d
		v.week_valuation = d
		v.month_valuation = d
		v.year_valuation = d
		v.save()
		msg = 'You have successfully reset your portfolio.'
	else:
		msg = 'It appears you are attempting to reset your portfolio. Try the "Account" button at the top of the page.'
	return base_view(request, msg)


class MakeProfile(ActivationView):
	def activate(self, request, activation_key):
		m = 1000000.00
		d = datetime_now()
		with transaction.atomic():
			active = ActivationView.activate(self, request, activation_key)
			if active:
				u = active.username
				p = Portfolio(username=u, money=m, add_date=d)
				p.save()
				m = 1000000.00
				v = Valuation(user=p, current_valuation=m, day_valuation=m,
					week_valuation=m, month_valuation=m, year_valuation=m)
				v.save()
			return active
	
	#This shouldn't be necessary, but can't hurt...
	def get_success_url(self, request, user):
		return 'registration_activation_complete', (), {}


@login_required
def base_view(request, message=''):
	user = request.user
	context = {}
	if user.is_authenticated():
		context["message"] = message
		user_entry = Portfolio.objects.get(username=user)
		context["money"] = "{0:.2f}".format(user_entry.money)
		context["valuation"] = "{0:.2f}".format(get_valuation(user))
		user_stocks = Owned.objects.filter(user=user_entry).order_by("symbol")
		symbols = [str(s.symbol) for s in user_stocks]
		prices = get_prices(symbols)
		stock_list = []
		for s in user_stocks:
			#p_value = int(s.quantity) * float(s.purchase_price)
			symbol = s.symbol
			q = s.quantity
			avg_price = float(s.avg_price)
			curr_price = avg_price
			try:
				curr_price = prices[symbol]
			except (KeyError, ValueError) as e:
				try:
					curr_price = get_price(s)
				except:
					pass
			curr_value = int(q) * curr_price
			profit = curr_value - int(q) * avg_price
			if avg_price == 0:
				#TODO: avoiding div by 0??
				gain = 100.0
			else:
				gain = ((curr_price / avg_price) - 1.0) * 100.0
			#convert to strings, to 2 decimal places.
			#TODO: put in commas (thousand, million, ...)
			avg_str = "$ {0:.2f}".format(avg_price)
			price_str = "$ {0:.2f}".format(curr_price)
			val_str = "$ {0:.2f}".format(curr_value)
			profit_str = "$ {0:.2f}".format(profit)
			gain_str = "{0:.1f} %".format(gain)
			stock_list.append([symbol, q, avg_str, price_str, val_str, profit_str, gain_str])
		context["stock_list"] = stock_list
	return render(request, 'portfolio/portfolio.html', context)


@login_required
def watchlist_view(request):
	if request.method == 'POST':
		u = request.user
		symbol = request.POST["symbol"]
		if not unwatch(u, symbol):
			#return HttpResponseRedirect('/failure/')
			pass
	user = request.user
	context = {}
	if user.is_authenticated():
		user_entry = Portfolio.objects.get(username=user)
		user_stocks = Watchlist.objects.filter(user=user_entry).order_by("symbol")
		context["user_stocks"] = user_stocks
	return render(request, 'portfolio/watchlist.html', context)


@login_required
def history_view(request):
	user = request.user
	context = {}
	if user.is_authenticated():
		user_entry = Portfolio.objects.get(username=user)
		db_stocks = Transaction.objects.filter(user=user_entry).order_by("date")
		user_stocks = []
		for s in db_stocks:
			trans_str = "Sell"
			if s.buy:
				trans_str = "Buy"
			table_entries = [str(x) for x in [s.symbol, s.quantity, s.price,
				s.date.strftime("%d %b %Y - %H:%M"), trans_str]]
			user_stocks.append(table_entries)
		context["user_stocks"] = user_stocks
	return render(request, 'portfolio/history.html', context)

