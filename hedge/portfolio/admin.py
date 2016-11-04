from django.contrib import admin
from .models import Portfolio, Transaction, Owned, Watchlist

admin.site.register(Portfolio)
admin.site.register(Transaction)
admin.site.register(Owned)
admin.site.register(Watchlist)
