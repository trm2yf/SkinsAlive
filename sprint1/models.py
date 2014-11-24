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
# Create your models here.
# from Crypto import Random
# from Crypto.Cipher import AES
#
# def pad(s):
#     return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
#
# def encrypt(message, key, key_size=256):
#     if key is None:
#         key = Random.new().read(key_size // 8)
#     message = pad(message)
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     return iv + cipher.encrypt(message)
#
# def decrypt(ciphertext, key):
#     iv = ciphertext[:AES.block_size]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     plaintext = cipher.decrypt(ciphertext[AES.block_size:])
#     return plaintext.rstrip(b"\0")
#
# def encrypt_file(file_name, key):
#     print 'Encrypt called'
#     with file_name as fo:
#         plaintext = fo.read()
#     enc = encrypt(plaintext, key)
#     # fo=open('E'+file_name.name.split("/")[-1], 'wb')
#     # fo.write(enc)
#     # fo.close()
#     return enc
#
# def decrypt_file(file_name, key):
#     with open(file_name, 'rb') as fo:
#         ciphertext = fo.read()
#     dec = decrypt(ciphertext, key)
#     with open(file_name[:-4], 'wb') as fo:
#         fo.write(dec)

from Crypto import Random
from Crypto.Cipher import AES

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    if key is None:
        key = Random.new().read(key_size // 8)
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    print 'Encrypt called'
    with open(file_name,'r') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    #file_name.close()
    overwrite=open(file_name,'wb')
    overwrite.write(enc)
    overwrite.close()
    # fo=open('E'+file_name.name.split("/")[-1], 'wb')
    # fo.write(enc)
    # fo.close()

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)

def filepath_handler(instance,name):
    return path.join('user_%d'%instance.posted_bulletin.author.id,'bulletin_%d'%instance.posted_bulletin.b_key,name)


# Document Model
class Document(models.Model):
    posted_bulletin=models.ForeignKey(Bulletin)
    docfile = models.FileField(upload_to=filepath_handler)
    d_key = models.AutoField(primary_key=True)
    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        #print self.docfile.name
        snake=path.join(getcwd(),'media',self.docfile.name)
        encrypt_file(snake,None)
        #self.docfile=ContentFile.open(ContentFile(self.docfile),)

        # print 'save called'
        # super(Document, self).save(*args, **kwargs)
        # print self.docfile
        # name=self.docfile.file.name
        # print name
        # snake=path.join(getcwd(),'media',name)
        # enc=encrypt_file(ContentFile(open(snake)),None)
        #
        # with open(path.join(getcwd(),'media',name),'w') as f:
        #     f.write(enc)
        # if not self.docfile:
        #     self.docfile.save(name=name,content=ContentFile(open(snake)), save=False)
        #     #self.docfile.close()
        #     #self.docfile=ContentFile(open(snake))
        # print 'Done'




