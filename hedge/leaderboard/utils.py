
from decimal import Decimal
from django.db import transaction
from .models import Valuation
from portfolio.models import Portfolio, Owned
from common.utils import get_price, get_prices


def view_helper(view="base"):
	valuations = Valuation.objects.all()
	leaders = []
	for v in valuations:
		name = v.user.username
		start = Decimal(1000000.00)
		current = v.current_valuation
		if view == "day":
			start = v.day_valuation
		elif view == "week":
			start = v.week_valuation
		elif view == "month":
			start = v.month_valuation
		elif view == "year":
			start = v.year_valuation
		increase = current - start
		leaders.append([name, start, current, increase])
	headings = ["Username:", "Initial:", "Current:", "Total Gain:"]
	title = 'All-time Leaders'
	if view != "base":
		headings[1] = view.capitalize() + " start:"
	if view == "day":
		title = 'Biggest gainers today'
	elif view == "week":
		title = 'Biggest gainers this week'
	elif view == "month":
		title = 'Biggest gainers this month'
	elif view == "year":
		title = 'Biggest gainers this year'
	leader_list = [headings] + sorted(leaders, key=lambda x:x[3], reverse=True)[:20]
	return {"title_str" : title, "leaders" : leader_list}


def update_vals(current=False, day=False, week=False, month=False, year=False):
	"""Updates rows for all users based on their current valuation.
	The arguments decide whether each specific entry is updated.
	For now this is called manually (superuser access ../leaderboard/update/#)
	"""
	#TODO:
	#  performance test and refactor...
	#  As it is, this will be pretty intensive on the DB.
	#  the task locks the Valuations table, and performs this atomically.
	#  I'm not sure how to do it better...
	symbols = []
	with transaction.atomic():
		stocks = Owned.objects.all()
		symbols = list(set(str(s.symbol).upper() for s in stocks))
	if not symbols:
		return "Error collecting symbols."
	prices = get_prices(symbols)
	if symbols and not prices:
		return "Failed to gather prices."
	with transaction.atomic():
		portfolios = Portfolio.objects.all()
		for port in portfolios:
			owned = Owned.objects.filter(user=port)
			current_valuation = float(port.money)
			for stock in owned:
				price = 0.0
				try:
					price = prices[stock.symbol]
				except (KeyError, ValueError) as e:
					try:
						price = get_price(s)
					except:
						pass
				current_valuation += stock.quantity * price
			val_entry = Valuation.objects.get(user=port)
			if current:
				val_entry.current_valuation = current_valuation
			if day:
				val_entry.day_valuation = current_valuation
			if week:
				val_entry.week_valuation = current_valuation
			if month:
				val_entry.month_valuation = current_valuation
			if year:
				val_entry.year_valuation = current_valuation
			val_entry.save()
		return "Successful update."


