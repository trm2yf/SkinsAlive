
from django import forms

from models import Skin,Document

from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file'
    )
    class Meta:
        model=Document
        fields=['docfile']

class SForm(forms.ModelForm):
    bulfile = forms.FileField(
        label='Select a skin'
    )
    class Meta:
        model=Skin
        fields=['bulfile']
        
class AddBulForm(forms.ModelForm):
    bulletin = forms.CharField(label='Enter a skin', max_length=100)
    class Meta:
        model=Skin
        fields=['bulletin']


class SkinForm(forms.ModelForm):
    class Meta:
        model=Skin
        fields=['title','text_description']
    def __init__(self, user,*args, **kwargs):
        forms.ModelForm.__init__(self,*args, **kwargs)


class AccountForm(forms.Form):
    username=forms.CharField(
        label='Username'
    )
    password=forms.CharField(label='Password',widget=forms.PasswordInput())
    email=forms.CharField(label='Email',widget=forms.EmailInput())
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    author = forms.BooleanField(required=False,label='Skin Designer')

    #nested Meta class
    class Meta:
        model = User
        fields = ('username', 'password')
