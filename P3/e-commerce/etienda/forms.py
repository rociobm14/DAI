from django import forms
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def validate_name(value):
    if not value[0].isupper():
        logger.error("The name must start with capital letters.")
        raise ValidationError("The name must start with capital letters.")
    
class ProductoForm(forms.Form):
    nombre = forms.CharField(label='Name', max_length=100, validators=[validate_name])
    precio = forms.FloatField(label='Price')
    descripción = forms.CharField(label='Description', max_length=500)
    categoría = forms.CharField(label='Category', max_length=100)
    imágen = forms.FileField(label='Image')