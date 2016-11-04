
import datetime
from urllib.error import HTTPError
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from common.utils import get_quote, fix_dot_dash, get_screen, bitcoin_price, get_hot_stocks
from .forms import QuantityForm
from portfolio.models import Portfolio, Owned, Watchlist
from portfolio.utils import buy, sell, watch, unwatch
from portfolio.views import base_view as portfolio_view


def base_view(request, message=''):
	UA_string = str(request.META["HTTP_USER_AGENT"]).lower()
	mobiles = ['mobile', 'iphone', 'android', 'fennec']
	mobile = False
	if any(m in UA_string for m in mobiles):
		mobile = True
	actives, gainers, losers = get_hot_stocks(mobile)
	context = {
		"actives" : actives,
		"gainers" : gainers,
		"losers" : losers,
		"message" : message
	}
	return render(request, 'stocks/stocks_main.html', context)


def symbol_view(request, symbol):
	symbol = symbol.upper()
	symbol = fix_dot_dash(symbol)
	if symbol not in settings.SYMBOLS:
		return base_view(request, 'Stock symbol: {} could not be found.'.format(symbol))
	message = ''
	if request.method == 'POST':
		u = request.user
		if request.POST["type"] == 'watch':
			if watch(u, symbol):
				return HttpResponseRedirect('/portfolio/watchlist')
		elif request.POST["type"] == 'unwatch':
			if unwatch(u, symbol):
				return HttpResponseRedirect('/portfolio/watchlist')
		q_form = QuantityForm(request.POST)
		if q_form.is_valid():
			q = q_form.cleaned_data["quantity"]
			if request.POST["type"] == 'buy':
				status, message = buy(u, q, symbol)
				if status:
					return portfolio_view(request, message)
				else:
					buy_form = QuantityForm()
			elif request.POST["type"] == 'sell':
				status, message = sell(u, q, symbol)
				if status:
					return portfolio_view(request, message)
				else:
					buy_form = QuantityForm()
		else:
			message = "Invalid number entered."
			buy_form = QuantityForm()
	else: # GET
		buy_form = QuantityForm()
	context = {'buy_form':buy_form, "owns":False, "watched":False, "message":message}
	#see if owned, add sell form
	if request.user.is_authenticated():
		#TODO: with suppress(KeyError, DoesNotExist):
		try:
			user_entry = Portfolio.objects.get(username=request.user)
			context["money"] = user_entry.money
			try:
				owned_entry = Owned.objects.get(user=user_entry, symbol=symbol)
				num_owned = owned_entry.quantity
				context["sell_form"] = QuantityForm(max_val=num_owned)
				context["num_owned"] = num_owned
				context["owns"] = True
			except:
				pass
			try:
				watched_entry = Watchlist.objects.get(user=user_entry, symbol=symbol)
				context["watched"] = True
			except:
				pass
		except:
			pass
	try:
		q = get_quote(symbol)
		if not q:
			with open('logs/failures.log', 'a') as f:
				f.write('Failed to scrape symbol: {}'.format(symbol))
			return base_view(request, 'Stock symbol: {} could not be found.'.format(symbol))
		context.update(q)
	except HTTPError as e:
		response = "Unable to find a quote for: " + symbol + "<br>"
		response += "Exception: " + str(e)
		raise Http404(response)
	context["symbol"] = symbol
	context["date"] = str(datetime.date.today())
	return render(request, 'stocks/stocks_stock.html', context)


def symbol_search(request):
	symbol = request.GET["symbol"]
	if symbol:
		return symbol_view(request, symbol)
	else:
		return base_view(request)


def screener_view(request, descending='', sort_by=''):
	options = ["ticker", "company", "marketcap", "pe", "eps", "volume", "price", "change"]
	table_labels = ["Symbol", "Company", "Market Cap", "P/E", "EPS",
		"Volume", "Price", "% Change"]
	if not sort_by:
		descending = '-'
		sort_by = 'change'
	table_entries = get_screen(options[2:], sort_by, descending)
	# For switching sort order in the template:
	if sort_by and descending:
		descending = '-'
	else:
		descending = ''
	context = {
		"columns" : zip(options, table_labels),
		"table_entries" : table_entries,
		"descending" : descending,
		"sort_by" : sort_by
	}
	return render(request, 'stocks/stocks_screener.html', context)


def bitcoin_view(request):
	# if request.method == 'POST':
	# 	u = request.user
	# 	q_form = QuantityForm(request.POST)
	# 	if q_form.is_valid():
	# 		q = q_form.cleaned_data["quantity"]
	# 		if request.POST["type"] == 'buy':
	# 			if buy(u, q, symbol):
	# 				return HttpResponseRedirect('/portfolio/')
	# 			else:
	# 				_write("error in buy")
	# 		elif request.POST["type"] == 'sell':
	# 			if sell(u, q, symbol):
	# 				return HttpResponseRedirect('/portfolio/')
	# 			else:
	# 				_write("error in sell")
	# 	else:
	# 		_write("invalid form")
	# 	#TODO: not HttpResponseRedirect.
	# 	return HttpResponseRedirect('/failure/')
	#else: # GET
	buy_form = QuantityForm()
	context = {"buy_form":buy_form, "owns":False}
	#see if owned, add sell form
	# if request.user.is_authenticated():
	# 	#TODO: with suppress(KeyError, DoesNotExist):
	# 	try:
	# 		user_entry = Portfolio.objects.get(username=request.user)
	# 		try:
	# 			owned_entry = Owned.objects.get(user=user_entry, symbol=symbol)
	# 			num_owned = owned_entry.quantity
	# 			context["sell_form"] = QuantityForm(max_val=num_owned)
	# 			context["num_owned"] = num_owned
	# 			context["owns"] = True
	# 		except:
	# 			pass
	# 		try:
	# 			watched_entry = Watchlist.objects.get(user=user_entry, symbol=symbol)
	# 			context["watched"] = True
	# 		except:
	# 			pass
	# 	except:
	# 		pass

	context["price"] = bitcoin_price()
	return render(request, 'stocks/stocks_bitcoin.html', context)
