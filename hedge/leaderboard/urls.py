from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.base_view, name='base_view'),
	url(r'^year$', views.year_view, name='year_view'),
	url(r'^month$', views.month_view, name='month_view'),
	url(r'^week$', views.week_view, name='week_view'),
	url(r'^day$', views.day_view, name='day_view'),
	url(r'^update=(?P<switch>\d)$', views.update, name='update')
]