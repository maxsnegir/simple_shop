from django import forms
from django.core.exceptions import ValidationError

from products.models import Product


class CreateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'description', 'subcategory',
                  'color', 'image', 'availability', ]

    def clean_price(self):
        price = self.cleaned_data['price']
        if int(price) < 0:
            return ValidationError('Цена не может быть отрицательной')
        return price
