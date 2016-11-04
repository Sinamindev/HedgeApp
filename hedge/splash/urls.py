from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.base_view, name='base_view'),
	url(r'^glossary', views.glossary_view, name='glossary_view'),
]