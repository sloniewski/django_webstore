from django import forms
from .validators import (
        validate_product_exits,
        validate_not_null,
        validate_product_quantity,
    )


class ItemForm(forms.Form):
    item = forms.IntegerField(
        validators=[
            validate_product_exits,
            validate_not_null,
        ]
    )
    qty = forms.IntegerField(
        min_value=0,
        validators=[
            validate_not_null,
        ]
    )
