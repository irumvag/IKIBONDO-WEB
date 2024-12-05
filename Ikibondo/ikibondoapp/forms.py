from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=Myuser
        fields=['phone_number','email','first_name', 'last_name','role','gender','password1','password2']
        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise forms.ValidationError("Phone number must be exactly 10 digits.")
            return phone_number
class CHWCreationForm(forms.ModelForm):
    class Meta:
        model=CHW
        fields=['LocationId','HID']
class Addlocation(forms.ModelForm):
    class Meta:
        model=Location
        fields=['LocationId','Country','Provence','District','Village','Streetcode']