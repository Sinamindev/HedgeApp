import json
from csv import reader
from decimal import Decimal
from contextlib import suppress
from urllib.request import urlopen
from urllib.error import URLError
from random import sample
from django.conf import settings
from django.core.cache import caches
#from django.contrib.sites.models import Site
from bs4 import BeautifulSoup as Soup
from datetime import datetime, timedelta
from portfolio.models import Owned

# TODO: multiprocessing Lock on certain things here?


# not sure why this was here...
# def get_domain():
# 	return Site.objects.get_current().domain


def get_ticker_symbols():
	ticker_symbols = caches["ticker_symbols"].get("symbols")
	if not ticker_symbols:
		owned_entries = Owned.objects.all()
		new_symbols = [o.symbol for o in owned_entries]
		hots = get_hot_stocks()
		for table in hots:
			for row in table:
				new_symbols.append(row[0])
		new_symbols = list(set(new_symbols))
		percents = {}
		if len(new_symbols) > 100:
		# segment the symbols... scrape_percents can handle 100 at a time
			for segment in [new_symbols[i:i+100] for i in range(0, len(new_symbols), 100)]:
				percents.update(scrape_percents(segment))
		elif needed:
			percents = scrape_percents(needed)
		ticker_symbols = []
		for k, v in percents.items():
			float_val = 0
			try:
				float_val = float(v)
			except ValueError:
				pass
			positive = float_val >= 0
			ticker_symbols.append((positive, k, v))
		caches["ticker_symbols"].set("symbols", ticker_symbols, 900)
	selected = sample(ticker_symbols, min(len(ticker_symbols), 30))
	return selected


def scrape_percents(symbols):
	symbol_str = ','.join(symbols)
	url = 'http://finance.google.com/finance/info?q=' + symbol_str
	page = get_page(url)
	json_str = page.decode('ascii', 'ignore').strip()[3:]
	data = json.loads(json_str)
	percents = dict([(d["t"], d["cp"]) for d in data])
	return percents


def flush_cache():
	caches["default"].clear()
	caches["prices"].clear()
	caches["quotes"].clear()
	caches["hot_stocks"].clear()
	caches["ticker_symbols"].clear()


def money_string(money):
	# Attempt to convert strings to float first.
	# will raise all kinds of errors for bad strings...
	if type(money) == str:
		try:
			money = float(money)
		except:
			money = float(''.join(money.split(',')))
	elif type(money) == int or type(money) == Decimal:
		money = float(money)
	elif type(money) != float:
		raise ValueError("Invalid type for 'money': {}".format(type(money)))
	return '{0:,.2f}'.format(money)


def fix_dot_dash(symbol):
	if '.' in symbol:
		if symbol not in settings.SYMBOLS and symbol.replace('.', '-') in settings.SYMBOLS:
			symbol = symbol.replace('.', '-')
	elif '-' in symbol:
		if symbol not in settings.SYMBOLS and symbol.replace('-', '.') in settings.SYMBOLS:
			symbol = symbol.replace('-', '.')
	return symbol


def get_page(url):
	response = urlopen(url)
	if response.code != 200:
		raise Exception("Problem reading webpage...")
	return response.read()


def get_prices(symbols):
	if not symbols:
		return {}
	needed = []
	prices = caches["prices"].get_many(symbols)
	for symbol in symbols:
		if symbol not in prices:
			needed.append(symbol)
	new_prices = {}
	if len(needed) > 100:
		# segment the symbols... scrape_prices can handle 100 at a time
		for segment in [needed[i:i+100] for i in range(0, len(needed), 100)]:
			new_prices.update(scrape_prices(segment))
	elif needed:
		new_prices = scrape_prices(needed)
	prices.update(new_prices)
	caches["prices"].set_many(new_prices, 60)
	return prices


def scrape_prices(symbols):
	symbol_str = ','.join(symbols)
	url = 'http://finance.google.com/finance/info?q=' + symbol_str
	page = get_page(url)
	json_str = page.decode('ascii', 'ignore').strip()[3:]
	data = json.loads(json_str)
	prices = dict([(d["t"], float(d["l_fix"])) for d in data])
	return prices


def get_price(symbol):
	if not symbol:
		return 0.0
	price = caches["prices"].get(symbol)
	if not price:
		url = 'http://finance.google.com/finance/info?q=' + str(symbol)
		page = get_page(url)
		json_str = page.decode('ascii', 'ignore').strip()[3:]
		data = json.loads(json_str)
		price = float(data[0]["l_fix"])
		caches["prices"].set(symbol, price, 60)
	return price


def finviz_quote(symbol):
	url = 'http://www.finviz.com/quote.ashx?t=' + symbol
	response_contents = get_page(url)
	#save_data_to_file(response_contents, 'quote.html')
	soup = Soup(response_contents, "lxml")
	company = soup.find('table', 'fullview-title').findAll('tr')[1].text
	table = soup.find('table', 'snapshot-table2')
	entries = [td.text for td in table.findAll('td')]
	d = dict(zip(*[iter(entries)]*2)) #haxxor 1337
	change = "{0:.2f}".format(float(d['Price']) - float(d['Prev Close']))
	low52, high52 = [x.strip() for x in d['52W Range'].split('-')]
	vol = ''.join(d['Volume'].split(','))
	avg_vol = d['Avg Volume']
	if avg_vol.endswith('K'):
		avg_vol = str(int(float(avg_vol[:-1]) * 1000))
	if avg_vol.endswith('M'):
		avg_vol = str(int(float(avg_vol[:-1]) * 1000000))
	if avg_vol.endswith('B'):
		avg_vol = str(int(float(avg_vol[:-1]) * 1000000000))
	keys = ['q_name', 'q_price', 'q_change', 'q_pchange', 'q_vol',
		'q_avgvol', 'q_mcap', 'q_pe', 'q_eps', 'q_close', 'q_open',
		'q_yhigh', 'q_ylow']
	vals = [company, d['Price'], change, d['Change'], vol,
		avg_vol, d['Market Cap'], d['P/E'], d['EPS (ttm)'],
		d['Prev Close'], '-', high52, low52]
	return dict(zip(keys, vals))


#http://finance.yahoo.com/d/quotes.csv?s=GOOG&f=nl1c1p2va2j1repokj
def yahoo_quote(symbol):
	url = 'http://finance.yahoo.com/d/quotes.csv?s='
	url += symbol
	url += '&f=nl1c1p2va2j1repokj'
	csvs = get_page(url).decode('ascii').strip()
	values = []
	for v in reader([csvs]).__next__():
		values.append(v)
	keys = ['q_name', 'q_price', 'q_change', 'q_pchange', 'q_vol',
		'q_avgvol', 'q_mcap', 'q_pe', 'q_eps', 'q_close', 'q_open',
		'q_yhigh', 'q_ylow']
	return dict(zip(keys, values))


def yql_quote(symbol):
	url = (
		"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yaho"
		"o.finance.quotes%20where%20symbol%20in%20(%22{0}%22)&format=json&dia"
		"gnostics=false&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&"
		"callback="
		).format(symbol)
	page = get_page(url).decode('ascii', 'ignore').strip()
	d = json.loads(page)["query"]["results"]["quote"]
	keys = ['q_name', 'q_price', 'q_change', 'q_pchange', 'q_vol',
		'q_avgvol', 'q_mcap', 'q_pe', 'q_eps', 'q_close', 'q_open',
		'q_yhigh', 'q_ylow']
	vals = [d['Name'], d['LastTradePriceOnly'], d['Change'], d['ChangeinPercent'], d['Volume'],
		d["AverageDailyVolume"], d['MarketCapitalization'], d['PERatio'], d['EarningsShare'],
		d['PreviousClose'], d["Open"], d["YearHigh"], d["YearLow"]]
	return dict(zip(keys, vals))


def goog_quote(symbol):
	url = "http://www.google.com/finance/info?infotype=infoquoteall&q={}".format(symbol)
	page = get_page(url)
	json_str = page.decode('ascii', 'ignore').strip()[3:]
	d = json.loads(json_str)[0]
	keys = ['q_name', 'q_price', 'q_change', 'q_pchange', 'q_vol',
		'q_avgvol', 'q_mcap', 'q_pe', 'q_eps', 'q_close', 'q_open',
		'q_yhigh', 'q_ylow']
	vals = [d['name'], d['l_fix'], d['c'], d['cp'], d['vo'],
		d["avvo"], d['mc'], d['pe'], d['eps'],
		d['pcls_fix'], d["op"], d["hi"], d["lo"]]
	return dict(zip(keys, vals))


def get_quote(symbol):
	"""Returns dict of 'q_name', 'q_price', 'q_change', 'q_pchange', 'q_vol',
		'q_avgvol', 'q_mcap', 'q_pe', 'q_eps', 'q_close', 'q_open',
		'q_yhigh', and 'q_ylow'
		for the given symbol.
	"""
	symbol = symbol.upper()
	if symbol not in settings.SYMBOLS:
		return {}
	if '.' in symbol:
		symbol = symbol.replace('.', '-')
	q = caches["quotes"].get(symbol)
	# Try yahoo, yql, google, finviz - return on first successful quote.
	if q:
		return q
	else:
		for scraper in [yahoo_quote, yql_quote, goog_quote, finviz_quote]:
			with suppress(URLError, ValueError, KeyError, TypeError):
				q = scraper(symbol)
				price = float(q['q_price'])
				caches["quotes"].set(symbol, q, 120)
				return q
	return {}


def get_screen(options, sort_by='', descending=False):
	option_map = {
		"marketcap" : "6",
		"pe" : "7",
		"eps" : "16",
		"sharesoutstanding" : "24",
		"roi" : "34",
		"perf13w" : "44",
		"perf52w" : "46",
		"high52w" : "57",
		"low52w" : "58",
		"price" : "65",
		"change" : "66",
		"volume" : "67",
		"targetprice" : "69"
	}
	opt_str = '1,2'
	for opt in options:
		opt_str += ',' + option_map[opt]
	sort_str = ''
	if descending:
		sort_str = '-'
	if sort_by:
		sort_str += sort_by
	url = "http://www.finviz.com/screener.ashx?v=152&o={0}&c={1}".format(sort_str, opt_str)
	response_contents = get_page(url)
	soup = Soup(response_contents, "lxml")
	table = soup.findAll('table')[9]
	rows = [[td.text for td in tr.findAll('td')] for tr in table.findAll('tr')][1:]
	return rows


def get_hot_stocks(mobile=False):
	actives = caches["hot_stocks"].get('actives')
	gainers = caches["hot_stocks"].get('gainers')
	losers = caches["hot_stocks"].get('losers')
	if not actives:
		actives = wsj_scrape("http://www.wsj.com/mdc/public/page/2_3021-activcomp-actives.html")
		if actives:
			caches["hot_stocks"].set('actives', actives, 3600)
		else:
			actives = []
	if not gainers:
		gainers = wsj_scrape("http://www.wsj.com/mdc/public/page/2_3021-gaincomp-gainer.html")
		if gainers:
			caches["hot_stocks"].set('gainers', gainers, 3600)
		else:
			gainers = []
	if not losers:
		losers = wsj_scrape("http://www.wsj.com/mdc/public/page/2_3021-losecomp-gainer.html")
		if losers:
			caches["hot_stocks"].set('losers', losers, 3600)
		else:
			losers = []
	if mobile:
		actives, gainers, losers = (list(x) if x else [] for x in [actives, gainers, losers])
		for table in [actives, gainers, losers]:
			if table:
				for row in table:
					row[1] = row[1][:32]
	return actives, gainers, losers


def wsj_scrape(url):
	response_contents = get_page(url)
	soup = Soup(response_contents, "lxml")
	table = soup.find('table', 'mdcTable')
	if not table:
		response_contents = get_page(url)
		soup = Soup(response_contents, "lxml")
		table = soup.find('table', 'mdcTable')
		if not table:
			return {}
	rows = [[td.text for td in tr.findAll('td')] for tr in table.findAll('tr')][1:]
	rows2 = []
	for row in rows:#[:10]:
		name, symbol = row[1].rsplit('(', 1)
		name = name.strip()[:72]
		symbol = symbol.strip().strip(')')
		if symbol not in settings.SYMBOLS:
			continue
		if 'actives' in url:
			rows2.append([symbol, name] + row[3:] + [row[2]])
		else:
			rows2.append([symbol, name] + row[2:])
	return rows2


def bitcoin_price():
	url = 'https://api.bitcoinaverage.com/ticker/USD/last'
	last_price = float(get_page(url).decode('ascii').strip())
	return last_price



