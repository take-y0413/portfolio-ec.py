from django import forms
from .models import CartUnit

class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=128)


class CartUnitForm(forms.ModelForm):
    class Meta:
        model = CartUnit
        fields = ('quantity',)
