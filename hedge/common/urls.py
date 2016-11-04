from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^user/$', views.check_username, name='check_username'),
]
