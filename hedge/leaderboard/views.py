
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Valuation
from .utils import update_vals, view_helper


def base_view(request):
	context = view_helper()
	return render(request, 'leaderboard/leaderboard.html', context)


def year_view(request):
	context = view_helper("year")
	return render(request, 'leaderboard/leaderboard.html', context)


def month_view(request):
	context = view_helper("month")
	return render(request, 'leaderboard/leaderboard.html', context)


def week_view(request):
	context = view_helper("week")
	return render(request, 'leaderboard/leaderboard.html', context)


def day_view(request):
	context = view_helper("day")
	return render(request, 'leaderboard/leaderboard.html', context)


def update(request, switch):
	"""Allows superusers to update the leaderboards manually.
	switch codes:
		0 - update current
		1 - update day
		2 - update week
		3 - update month
		4 - update year
		5 = all
	More can be added, or a new method of grouping...
	For now these codes should be sufficient for manual updates.
	"""
	if not request.user.is_superuser:
		raise PermissionDenied
	current=day=week=month=year=False
	if switch == '0':
		current = True
	elif switch == '1':
		day = True
	elif switch == '2':
		week = True
	elif switch == '3':
		month = True
	elif switch == '4':
		year = True
	elif switch == '5':
		current=day=week=month=year=True
	else:
		return HttpResponse('skipped')
	msg = update_vals(current=current, day=day, week=week, month=month, year=year)
	return HttpResponse(msg)


