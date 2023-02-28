from django import forms
from .models import Product, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class  ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['number', 'tc_compra','tc_venta']

class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))


class ContactFormW(forms.Form):
    email = forms.EmailField(label='Email')
    numero = forms.IntegerField(label = "Numero",required = False,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))