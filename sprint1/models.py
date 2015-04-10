#imports
from django.db import models
import datetime
from os import urandom,path,getcwd
from hashlib import sha256
from base64 import urlsafe_b64encode
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import StringIO
from django.contrib.auth.models import User


class Author(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, unique=True)


# Skin Model
class Skin(models.Model):

    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    num_views = models.IntegerField(default=0)
    author= models.ForeignKey(User)
    b_key = models.AutoField(primary_key=True)

    def save(self):
        if not self.date_created:
            self.date_created = datetime.datetime.now()
        # self.date_modified = datetime.datetime.now()
        super(Skin, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.title


#def pad(s):
#   return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def filepath_handler(instance,name):
    return path.normpath(path.join('user_%d'%instance.posted_bulletin.author.id,'bulletin_%d'%instance.posted_bulletin.b_key,name))

class Key(models.Model):
    k_key=models.AutoField(primary_key=True)
    owner=models.ForeignKey(User)
    public=models.CharField(max_length=2048)

class Request(models.Model):
    owner = models.ForeignKey(User)
    text_description = models.TextField()
    imgfile = models.FileField(upload_to="images")


# Document Model
def keylookup(userobject):
    results=Key.objects.filter(owner__exact=userobject)
    for p in results:
        return p.public

class Document(models.Model):
    posted_bulletin=models.ForeignKey(Skin)
    docfile = models.FileField(upload_to=filepath_handler)
    d_key = models.AutoField(primary_key=True)


    def save(self,*args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        snake=path.join(getcwd(),'media',self.docfile.name)

