#imports
from django.db import models
import datetime
from django.contrib.auth.models import User

######  MODELS ######

# Folder Model
class Folder(models.Model):
    owner=models.ForeignKey(User)
    f_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    folder_contained=models.ForeignKey('self',blank=True,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name

# Bulletin Model
class Bulletin(models.Model):
    folder = models.ForeignKey(Folder)
    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    date_created = models.DateField(editable=False, default=datetime.datetime.today())
    date_modified = models.DateTimeField(editable=False, default=datetime.datetime.today())

    author= models.ForeignKey(User)
    lat = models.DecimalField(decimal_places=2,max_digits=10)
    long = models.DecimalField(decimal_places=2,max_digits=10)
    encrypted=models.BooleanField(default=True)
    b_key = models.AutoField(primary_key=True)

    def save(self):
        if not self.b_key:
            self.date_created = datetime.date.today()
        self.date_modified = datetime.datetime.today()
        super(Bulletin, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.title

# Document Model
class Document(models.Model):
    posted_bulletin=models.ForeignKey(Bulletin)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    d_key = models.AutoField(primary_key=True)

