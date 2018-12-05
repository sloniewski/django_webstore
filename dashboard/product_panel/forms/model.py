from django import forms

from webstore.product.models import Price


class PriceCreateForm(forms.ModelForm):

	class Meta:
		model = Price
		fields = [
			'value',
			'valid_from',
		]

	def __init__(self, *args, **kwargs):
		product = kwargs.pop('product')
		super().__init__(*args, **kwargs)
		self.product = product

	def save(self, *args, **kwargs):
		instance = super().save(commit=False)
		instance.product = self.product
		instance.save()
		return instance
