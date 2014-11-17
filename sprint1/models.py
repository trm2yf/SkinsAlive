from django.db import models
import datetime
from os import urandom
from hashlib import sha256
from base64 import urlsafe_b64encode
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
class Folder(models.Model):
    f_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    folder_contained=models.ForeignKey('self')
    def __str__(self):              # __unicode__ on Python 2
        return self.name
# Users Model
# class Users(AUser):
#     #username = models.CharField(max_length=16,unique=True)
#     #email = models.EmailField()
#     #password = models.CharField(max_length=2048)
#     role = models.CharField(max_length=2048)
#     p_salt=models.CharField(max_length=16)
#     u_key = models.AutoField(primary_key=True)
#     REQUIRED_FIELDS=['password','email']
#     USERNAME_FIELD='username'
#
#     objects = UserManager()
#     def set_password(self,inpass):
#         self.p_salt=urlsafe_b64encode(urandom(16))
#         self.password=sha256(self.p_salt+inpass)
#     def __str__(self):              # __unicode__ on Python 2
#         return self.u_name
# Bulletin Model
class Bulletin(models.Model):
    folder = models.ForeignKey(Folder)
    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    date_created = models.DateField(editable=False, default=datetime.datetime.today())
    date_modified = models.DateTimeField(editable=False, default=datetime.datetime.today())
    #authors = models.ManyToManyField(User)
    author= models.ForeignKey(User)
    lat = models.DecimalField(decimal_places=2,max_digits=10)
    long = models.DecimalField(decimal_places=2,max_digits=10)
    encrypted=models.BooleanField(default=True)
    b_key = models.AutoField(primary_key=True)
    #n_comments = models.IntegerField()
    #rating = models.IntegerField()
    def save(self):
        if not self.b_key:
            self.date_created = datetime.date.today()
        self.date_modified = datetime.datetime.today()
        super(Bulletin, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.title
# Create your models here.
class Document(models.Model):
    posted_bulletin=models.ForeignKey(Bulletin)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    d_key = models.AutoField(primary_key=True)

