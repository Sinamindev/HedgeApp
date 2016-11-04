"""hedge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from splash import urls as splash_urls
from common import urls as common_urls
from portfolio import urls as portfolio_urls
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from portfolio.views import MakeProfile
from stocks import urls as stocks_urls
from leaderboard import urls as leaderboard_urls
from account import urls as account_urls


urlpatterns = [
	url(r'^', include(splash_urls, namespace="splash")),
	url(r'^api/', include(common_urls, namespace="common")),
	url(r'^portfolio/', include(portfolio_urls, namespace="portfolio")),
	url(r'^accounts/manage/', include(account_urls, namespace="account")),
	url(r'^accounts/activate/complete/$', 
		TemplateView.as_view(template_name='registration/activation_complete.html'),
		name='registration_activation_complete'),
	url(r'^accounts/register/$', RegistrationView.as_view(
		form_class=RegistrationFormUniqueEmail), name='registration_register'),
	url(r'^accounts/activate/(?P<activation_key>\w+)/$', MakeProfile.as_view(),
		name='registration_activate'),
	url(r'^accounts/profile/$', include(portfolio_urls, namespace="portfolio")),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^stocks/', include(stocks_urls, namespace="stocks")),
	url(r'^leaderboard/', include(leaderboard_urls, namespace="leaderboard")),
	url(r'^admin/super-secret/', include(admin.site.urls))
]

