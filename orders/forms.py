from django import forms
from formset.widgets import DateTextbox
from .models import Order


class OrderForm(forms.ModelForm):
    """Form for creating new order."""
    class Meta:
        model = Order
        fields = ['table_number',]
        labels = {
            'table_number': 'Table Number',
        }
        error_messages = {
            'table_number':{
                'required': 'Please, enter the table number'
            }
        }


class ReportForm(forms.Form):
    """Form for generating report with chosen date."""
    date = forms.DateField(
        widget=DateTextbox,
        label="Choose date",
        error_messages={
            'required':'Please choose date for report'
        }
        )