
from decimal import Decimal
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from common.utils import get_price, get_prices, get_quote
from .models import Portfolio, Transaction, Owned, Watchlist
from django.utils.timezone import now
from datetime import datetime
from hashlib import md5


def hash_user(username):
	u = None
	try:
		u = User.objects.get(username=username)
	except:
		return None
	m = md5()
	user_info = "{}-{}-{}-{}".format("secret-key", u.get_full_name(), u.get_username(), u.email)
	m.update(bytes(user_info, encoding='utf-8'))
	hash_string = m.hexdigest()
	return hash_string
	

def get_valuation(username):
	"""Returns a user's total value (stocks and money)"""
	quantities = {}
	fallback_prices = {}
	value = 0
	# Load quantites
	with transaction.atomic():
		user = Portfolio.objects.get(username=username)
		value = user.money
		stocks = Owned.objects.filter(user=user)
		for stock in stocks:
			quantities[stock.symbol] = stock.quantity
			fallback_prices[stock.symbol] = stock.avg_price
	symbols = list(quantities.keys())
	if not symbols:
		return value
	prices = get_prices(symbols)
	for s in symbols:
		try:
			value += Decimal(prices[s]) * quantities[s]
		except (KeyError, ValueError) as e:
			try:
				price = get_price(s)
				value += Decimal(price) * quantities[s]
			except:
				value += fallback_prices[s] * quantities[s]
	return value

#not sure if this is working
def is_trading_hours(symbol):
	"""Returns True is the market is open
	-Some stocks are traded on markets with hours differing from Wall Street.
	"""
	#TODO: verify that datetime is using pacific time...
	# consider switching to now() = server time (should be pacific?)
	curr_time = datetime.now()
	#market closed thanksgivina and christmas and new year's.
	# TODO: update later for next year's holidays
	holidays = ((11, 26), (12, 25), (1, 1))
	today_tuple = (curr_time.month, curr_time.day)
	if today_tuple in holidays:
		return False
	elif curr_time.weekday() < 5 and curr_time.hour >= 6 and curr_time.hour < 13:
		if curr_time.hour == 6 and curr_time.minute < 30:
			return False
		return True
	else:
		return False


def _invalid_quantity(username, symbol, quantity):
	"""Returns True if quantity is not a valid number
	Quantity must be at least 1,
	and not more than the stock's daily volume
	"""
	#TODO: scrape quantity, or get it in the form ?? then implement actual check
	#TODO: factor in user's buy's from same day
	if quantity < 1:
		return True
	#volume = get_quote(symbol)...
	#user_transactions = Transaction.objects.filter(username...)
	#user_volume = sum(int(t.volume) for t in user_transactions)
	#if user_volume + quantity > volume:
	#	return True
	return False


def buy(username, quantity, symbol):
	"""Performs purchase of stock for given parameters.
	Utilizes atomic transaction so that the DB remains intact
	Returns False if the transaction failed.
	"""
	# Is the symbol valid, is the market open
	if symbol not in settings.SYMBOLS:
		return False, 'Invalid symbol.'
	elif not is_trading_hours(symbol):
		return False, """The market is currently closed. Market hours are 6:30am - 4:00pm EST."""
	# Try to scrape the price of the stock.
	price = 0.0
	try:
		price = get_price(symbol)
	except:
		return False, 'An error occurred.\nUnable to retrieve price information.'
	if price == 0.0:
		return False, 'An error occurred.\nUnable to retrieve price information.'# - price=0.0'
	total_cost = price * quantity
	# Determine whether quantity is valid
	if _invalid_quantity(username, symbol, quantity):
		return False, 'Invalid quantity supplied.'
	# Does the user already own some of this stock?
	user = Portfolio.objects.get(username=username)
	owned_entry = None
	try:
		owned_entry = Owned.objects.get(user=user, symbol=symbol)
	except ObjectDoesNotExist:
		pass
	# Make the transaction
	with transaction.atomic():
		# Determine whether the user can afford the purchase
		if user.money < total_cost:
			return False, 'Insufficient funds. Could not complete BUY order.'
		user.money -= Decimal(total_cost)
		trans = Transaction(user=user, symbol=symbol, quantity=quantity,
			price=price, date=now(), buy=True)
		if owned_entry:
			prev_q = owned_entry.quantity
			prev_p = float(owned_entry.avg_price)
			new_q = prev_q + quantity
			# for reference: total_cost = price * quantity
			new_p = Decimal((total_cost + prev_p*prev_q)/(float(new_q)))
			owned_entry.quantity = new_q
			owned_entry.avg_price = new_p
		else:
			owned_entry = Owned(user=user, symbol=symbol, quantity=quantity,
				avg_price=Decimal(price))
		user.save()
		trans.save()
		owned_entry.save()
	message = 'Successfully purchased {0} shares of {1} at {2:,.2f}/share ({3:,.2f} total).'.format(quantity, symbol, price, total_cost)
	return True, message


def sell(username, quantity, symbol):
	"""Performs sell of stock for given parameters.
	Utilizes atomic transaction so that the DB remains intact
	Returns False if the transaction failed.
	"""
	# Is the symbol valid, is the market open
	if symbol not in settings.SYMBOLS:
		return False, 'Invalid symbol.'
	elif not is_trading_hours(symbol):
		return False, """The market is currently closed. Market hours are 6:30am - 4:00pm EST."""
	# Try to scrape the price of the stock.
	price = 0.0
	try:
		price = get_price(symbol)
	except:
		return False, 'An error occurred.\nUnable to retrieve price information.'
	if price == 0.0:
		return False, 'An error occurred.\nUnable to retrieve price information.'
	total_cost = price * quantity
	# Determine whether the user owns the stock to sell
	user = Portfolio.objects.get(username=username)
	owned_entry = None
	try:
		owned_entry = Owned.objects.get(user=user, symbol=symbol)
	except ObjectDoesNotExist:
		return False, 'An error occurred.\nUnable to retrieve user stock information.'
	if owned_entry.quantity < quantity:
		return False, 'Invalid quantity supplied.'
	# Make the transaction
	with transaction.atomic():
		user.money += Decimal(total_cost)
		trans = Transaction(user=user, symbol=symbol, quantity=quantity,
			price=price, date=now(), buy=False)
		if owned_entry.quantity == quantity:
			owned_entry.delete()
		else:
			owned_entry.quantity -= quantity
			owned_entry.save()
		user.save()
		trans.save()
	message = 'Successfully sold {0} shares of {1} at {2:,.2f}/share ({3:,.2f} total).'.format(quantity, symbol, price, total_cost)
	return True, message


def watch(username, symbol):
	"""Add a stock symbol to a user's watchlist
	returns True if stock is added to watchlist
	"""
	#TODO: do we need to validate symbol?
	# Ensure symbol is nota already in watchlist
	user_entry = Portfolio.objects.get(username=username)
	try:
		#TODO: there's got to be a better way - exists(user, symbol)??
		owned_entry = Watchlist.objects.get(user=user_entry, symbol=symbol)
		if owned_entry:
			return False
	except ObjectDoesNotExist:
		pass
	# Get the company name
	quote = get_quote(symbol)
	name = quote["q_name"]
	# Create and save entry
	new_entry = Watchlist(user=user_entry, symbol=symbol, company=name)
	new_entry.save()
	return True


def unwatch(username, symbol):
	"""Remove a stock symbol from a user's watchlist
	returns True if stock is removed from watchlist
	"""
	# Get DB entry for watched stock
	owned_entry = None
	try:
		user_entry = Portfolio.objects.get(username=username)
		owned_entry = Watchlist.objects.get(user=user_entry, symbol=symbol)
	except ObjectDoesNotExist:
		return False
	# Remove entry
	if owned_entry:
		owned_entry.delete()
		return True
	else:
		return False



