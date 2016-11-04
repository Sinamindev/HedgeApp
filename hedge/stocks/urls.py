from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.base_view, name='base_view'),
	url(r'^screener/$', views.screener_view, name='screener_view'),
	url(r'^screener/(?P<descending>-)?(?P<sort_by>\w{1,20})$',
		views.screener_view, name='screener_view'),
	url(r'^symbol_search/$', views.symbol_search, name='symbol_search'),
	#url(r'^bitcoin$', views.bitcoin_view, name='bitcoin_view'),
	url(r'^(?P<symbol>[-\w\.]{1,8})$', views.symbol_view, name='symbol_view'),
]