__author__ = 'Zachary'
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
class AccountForm(forms.Form):
    username=forms.CharField(
        label='Username'
    )
    password=forms.CharField(label='Password',widget=forms.PasswordInput())
    email=forms.CharField(label='Email',widget=forms.EmailInput())
    
class UserForm(forms.ModelForm):
    password = forms.CahrField(widget=forms.PasswordInput())
    #nested Meta class
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
