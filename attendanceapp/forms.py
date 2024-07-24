from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import ModelChoiceField
# from dal import autocomplete
from .models import *

class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    period = forms.ChoiceField(choices=[(i, f'Period {i}') for i in range(1, 9)], required=False)