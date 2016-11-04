echo "Starting uwsgi server..."
uwsgi --ini ../server_settings/uwsgi_hedge.ini 1>logs/uwsgi_console.log 2>logs/uwsgi_console_err.log </dev/null &
sleep 3
tail logs/uwsgi_console_err.log
sleep 1
echo "Starting cron tasks..."
python3 manage.py run_huey 1>logs/huey_tasks.log 2>logs/huey_tasks_err.log </dev/null &
sleep 2
tail logs/huey_tasks_err.log
exit 0
