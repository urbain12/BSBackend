from django import forms
from .models import *

#empl form
class VaccineCreateForm(forms.ModelForm):
   class Meta:
     model = Vaccines
     fields = ['user','Vaxtype','Vaxplace']