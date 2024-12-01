from django.contrib.auth.forms import UserCreationForm
from .models import Myuser,CHW,Parent,Location
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=Myuser
        fields=['phone_number','email','first_name', 'last_name','password1','password2']
class CHWCreationForm(forms.ModelForm):
    class Meta:
        model=CHW
        fields=['NID','HID']
class Addlocation(forms.ModelForm):
    class Meta:
        model=Location
        fields=['LocationId','Country','Provence','District','Village','Streetcode']