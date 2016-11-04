
from datetime import datetime
from huey.djhuey import crontab, db_periodic_task
from .utils import update_vals
from common.utils import flush_cache


def _log(msg):
	time_str = '[{}] '.format(datetime.utcnow())
	with open('logs/cron_tasks.log', 'a') as f:
		f.write(time_str + msg + '\n')

# Clear the cache in the morning...
# hopefully this cleans up some of the problems...
@db_periodic_task(crontab(day_of_week='1-5', hour='14-22', minute='19'))
def flush_cache_hourly():
	flush_cache()
	#_log("flushed cache")

# Current
@db_periodic_task(crontab(minute='*/5', day_of_week='1-5', hour='14-21'))
def every_5_min():
	msg = update_vals(current=True)
	#_log(msg + "- leaderboard current")

# Day
@db_periodic_task(crontab(day_of_week='1-5', hour='14', minute='26'))
def monday_thru_friday_morning():
	msg = update_vals(day=True)
	_log(msg + "- leaderboard daily")

# Week
@db_periodic_task(crontab(day_of_week='1', hour='14', minute='27'))
def monday_morning():
	msg = update_vals(week=True)
	_log(msg + "- leaderboard weekly")

# Month
@db_periodic_task(crontab(day='1', hour='14', minute='28'))
def first_of_the_month():
	msg = update_vals(month=True)
	_log(msg + "- leaderboard monthly")

# Year
@db_periodic_task(crontab(month='1', day='1', hour='14', minute='29'))
def first_of_the_year():
	msg = update_vals(year=True)
	_log(msg + "- leaderboard yearly")
