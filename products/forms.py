from django import forms

from products.models import Product


class CreateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'description', 'subcategory',
                  'color', 'image', 'availability', ]
