from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from .forms import NameForm
from portfolio.utils import hash_user

@login_required
def base_view(request):
	bad_form = False
	name_form = NameForm()
	username = request.user.username
	u = User.objects.get(username=username)
	p = Portfolio.objects.get(username=username)
	if request.method == 'POST':
		name_form = NameForm(request.POST)
		if name_form.is_valid():
			first = name_form.cleaned_data["first_name"]
			last = name_form.cleaned_data["last_name"]
			u.first_name = first
			u.last_name = last
			u.save()
		else:
			bad_form = True
	deactivate_key = hash_user(username)
	context = {
		"bad_form": bad_form,
		"username": username,
		"email": u.email,
		"f_name": u.first_name,
		"l_name": u.last_name,
		"add_date": p.add_date,
		"form": name_form,
		"deac_key": deactivate_key
	}
	return render(request, 'account/manage.html', context)

