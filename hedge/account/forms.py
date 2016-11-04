
from django import forms


class NameForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()

