from django import forms
from .models import Team, pre_time_choice


class CreateForm(forms.Form):
    name = forms.CharField(max_length=20)
    intro = forms.CharField(max_length=50)
    code = forms.CharField(max_length=100)



