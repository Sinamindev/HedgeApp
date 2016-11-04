from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.base_view, name='base_view'),
	url(r'^watchlist$', views.watchlist_view, name='watchlist_view'),
	url(r'^history$', views.history_view, name='history_view'),
	url(r'^reset-portfolio/(?P<user_key>[0-9a-f]{32})$', views.reset_portfolio, name='reset_portfolio'),
	url(r'^deactivate/(?P<user_key>[0-9a-f]{32})$', views.deactivate, name='deactivate'),
]