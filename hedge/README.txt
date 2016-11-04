This is a somewhat functional prototype of the final site.
You will need to put "secrets.json" in the project directoy (alongside manage.py)

We have some stuff in a db, to sync with the git version:
-navigate to ../hedge/db/
$ psql -U root -d hedge_db -f db_dump

Then navigate to ../hedge/ and run (mightn't be necessary since you just synced db...):
$ python3 manage.py makemigrations
$ python3 managy.py migrate

And then fire up the server:
$ python3 manage.py runserver

And then check out some urls:
127.0.0.1:8000/
127.0.0.1:8000/portfolio
127.0.0.1:8000/portfolio/watchlist
127.0.0.1:8000/portfolio/history
127.0.0.1:8000/stocks
127.0.0.1:8000/stocks/GOOG
127.0.0.1:8000/stocks/screener
127.0.0.1:8000/stocks/screener/change
127.0.0.1:8000/leaderboard
127.0.0.1:8000/leaderboard/year
127.0.0.1:8000/leaderboard/month
127.0.0.1:8000/leaderboard/day






