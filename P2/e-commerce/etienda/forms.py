from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(label='Name', max_length=100)
    precio = forms.FloatField(label='Price')
    descripción = forms.CharField(label='Description', max_length=500)
    categoría = forms.CharField(label='Category', max_length=100)
    imágen = forms.FileField(label='Image')