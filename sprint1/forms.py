__author__ = 'Zachary'
from django import forms
from models import Bulletin
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
class BulletinForm(forms.ModelForm):
    # title=forms.CharField(label='Bulletin Title')
    # text_description=forms.CharField(label='Text Description')
    location=forms.CharField(label='City of Interest')
    # encrypted = forms.BooleanField()

    class Meta:
        model=Bulletin
        fields=['title','text_description','encrypted','folder']
    # def __init__(self):
    #         self.fields['encrypted'].initial= True
    """
    bulletin = models.ForeignKey(Folder)
    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Users)
    author_id = models.IntegerField()
    lat = models.DecimalField(decimal_places=2,max_digits=10)
    long = models.DecimalField(decimal_places=2,max_digits=10)
    """

class AccountForm(forms.Form):
    username=forms.CharField(
        label='Username'
    )
    password=forms.CharField(label='Password',widget=forms.PasswordInput())
    email=forms.CharField(label='Email',widget=forms.EmailInput())
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    #nested Meta class
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
