from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name
# Users Model
class Users(models.Model):
    u_name = models.CharField(max_length=16)
    email = models.EmailField()
    password = models.CharField()
    role = models.CharField()
    u_key = models.IntegerField()
    

    def __str__(self):              # __unicode__ on Python 2
        return self.u_name
# Bulletin Model
class Bulletin(models.Model):
    bulletin = models.ForeignKey(Bulletin)
    title = models.CharField(max_length=255)
    text_description = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    author_id = models.IntegerField()
    lat = models.DecimalField()
    long = models.DecimalField()
    
    #n_comments = models.IntegerField()
    #rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.title