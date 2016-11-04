
from django import forms


class QuantityForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=1000000000)
	def __init__(self, *args, max_val=None, **kwargs):
		super(QuantityForm, self).__init__(*args, **kwargs)
		if max_val:
			#self.fields["quantity"].widget.attrs.update({'min': min, 'max': max})
			self.fields["quantity"] = forms.IntegerField(min_value=1, max_value=max_val)
