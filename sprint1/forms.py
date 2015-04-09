__author__ = 'Zachary'
from django import forms

from models import Skin,Document,Folder

from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file'
    )
    class Meta:
        model=Document
        fields=['docfile']

class RequestForm(forms.Form):
    text_description = forms.CharField(label="Description Summary",widget=forms.Textarea)
    imgfile = forms.FileField(label="Submit a sketch?")

class SForm(forms.ModelForm):
    bulfile = forms.FileField(
        label='Select a skin'
    )
    class Meta:
        model=Skin
        fields=['bulfile']
        
class AddBulForm(forms.ModelForm):
    folder = forms.CharField(label='Enter a folder', max_length=100)
    bulletin = forms.CharField(label='Enter a skin', max_length=100)
    class Meta:
        model=Skin
        fields=['folder','bulletin']
# class PermissionForm(forms.ModelForm):
#     private= forms.FileField(
#         label='Share your private key'
#     )
#     class Meta:
#         model=Permission
#         fields=['permitted','private']

class FolderForm(forms.ModelForm):
    # title=forms.CharField(label='Skin Title')
    # text_description=forms.CharField(label='Text Description')
    class Meta:
        model=Folder
        fields=['name']
    #def __init__(self):
      #       self.fields['folder'].initial=1


class SkinForm(forms.ModelForm):
    # title=forms.CharField(label='Skin Title')
    # text_description=forms.CharField(label='Text Description')
    location=forms.CharField(label='City of Interest')
    # encrypted = forms.BooleanField()

    class Meta:
        model=Skin
        fields=['title','text_description']
    def __init__(self, user,*args, **kwargs):
        forms.ModelForm.__init__(self,*args, **kwargs)
        # try:
        #     self.fields['folder'].queryset = Folder.objects.filter(owner=user)
        # except Exception as e:
        #     print e
        #     pass
     #   self.fields['encrypted'].initial= True
      #       self.fields['folder'].initial=1
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
    author = forms.BooleanField(required=False)
    #Type = forms.ChoiceField(choices=('Author','Reader')) 

    #nested Meta class
    class Meta:
        model = User
        fields = ('username', 'password')
