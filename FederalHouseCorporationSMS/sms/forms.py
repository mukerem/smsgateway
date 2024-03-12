from django import forms
from sms.models import SMS

class SMSSend(forms.ModelForm):
    class Meta:
        model = SMS
        fields = ("text", "destination")

class DateFilter(forms.Form):
    
    date = forms.DateField(
        widget=forms.DateField,
        label="date",
        required=False,
    )