from django import forms

from webstore.core.widgets import MaterializeSelectMultiple
from webstore.product.models import Price, Gallery, Picture


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


class GalleryImageCreateForm(forms.Form):
	name = forms.CharField(max_length=128, required=True)
	picture = forms.ImageField()
	number = forms.IntegerField()

	def __init__(self, *args, **kwargs):
		product = kwargs.pop('product')
		self.product = product
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		picture = Picture.objects.create(
			name=self.cleaned_data['name'],
			data=self.cleaned_data['picture']
		)
		gallery = Gallery.objects.create(
			picture=picture,
			product=self.product,
			number=self.cleaned_data['number'],
		)
		return gallery


class GalleryImageChooseForm(forms.Form):
	picture = forms.ModelMultipleChoiceField(
		queryset=None,
	)

	def __init__(self, *args, **kwargs):
		product = kwargs.pop('product')
		self.product = product
		super().__init__(*args, **kwargs)
		self.fields['picture'].queryset = Picture.objects.all()

	def save(self):
		Gallery.objects.bulk_create(
			[Gallery(picture=x, product=self.product) for x in self.cleaned_data['picture']]
		)
		return self.product

