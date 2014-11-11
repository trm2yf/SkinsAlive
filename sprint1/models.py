from django.db import models
import datetime
class Folder(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    #folder_contained=models.ForeignKey(default=None)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
# Users Model
class Users(models.Model):
    u_name = models.CharField(max_length=16)
    email = models.EmailField()
    password = models.CharField(max_length=2048)
    role = models.CharField(max_length=2048)
    u_key = models.IntegerField()
    

    def __str__(self):              # __unicode__ on Python 2
        return self.u_name
# Bulletin Model
class Bulletin(models.Model):
    bulletin = models.ForeignKey(Folder)
    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    date_created = models.DateField(editable=False)
    date_modified = models.DateTimeField(editable=False)
    authors = models.ManyToManyField(Users)
    author_id = models.IntegerField()
    lat = models.DecimalField(decimal_places=2,max_digits=10)
    long = models.DecimalField(decimal_places=2,max_digits=10)
    encrypted=models.BooleanField(default=True)
    
    #n_comments = models.IntegerField()
    #rating = models.IntegerField()
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        super(Bulletin, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.title
# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

