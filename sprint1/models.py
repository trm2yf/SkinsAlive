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
# from Crypto import Random
# from Crypto.Cipher import AES

######  MODELS ######


#extending User object

# class UserProfile(models.Model):
#     author = models.BooleanField(default=True)
#     user = models.ForeignKey(User, unique=True, related_name='profile')


# Folder Model
#
# #extending User object
# class UserProfile(models.Model):
#     author = models.BooleanField(default=True)
#     user = models.ForeignKey(User, unique=True, related_name='profile')
#
# # Folder Model



class Folder(models.Model):
    owner=models.ForeignKey(User)
    f_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
  #  text_description = models.TextField(max_length=1024)
  #   folder_contained=models.ForeignKey('self',blank=True,null=True,limit_choices_to={'owner_id': User})
    def save(self):
        super(Folder, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.name



class Author(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, unique=True)


# Bulletin Model
class Bulletin(models.Model):
    folder = models.ForeignKey(Folder)
    title = models.CharField(max_length=255)
    text_description = models.TextField(max_length=1024)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    num_views = models.IntegerField(default=0)
    author= models.ForeignKey(User)
    lat = models.DecimalField(decimal_places=2,max_digits=10)
    long = models.DecimalField(decimal_places=2,max_digits=10)
    encrypted=models.BooleanField(default=True)
    b_key = models.AutoField(primary_key=True)

    def save(self):
        if not self.date_created:
            self.date_created = datetime.datetime.now()
        # self.date_modified = datetime.datetime.now()
        super(Bulletin, self).save()
    def __str__(self):              # __unicode__ on Python 2
        return self.title

# Create your models here.
from Crypto import Random,Util
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.PublicKey import RSA

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    if key is None:
        key = Random.new().read(key_size // 8)
    # message = pad(message)
    # iv = Random.new().read(RSA.block_size)
    # cipher = RSA.new(key, RSA.MODE_CBC, iv)
    # return iv + cipher.encrypt(message)
    key=RSA.importKey(key)
    cipher = PKCS1_OAEP.new(key)
    #print 'LENGTH',
    #print len(cipher._key)
    ciphertext=cipher.encrypt(message)
    #print len(ciphertext)
    return ciphertext

def decrypt(ciphertext, key):
    # iv = ciphertext[:RSA.block_size]
    # cipher = RSA.new(key, RSA.MODE_CBC, iv)
    # plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    # return plaintext.rstrip(b"\0")
    key=RSA.importKey(key,None)
    cipher = PKCS1_OAEP.new(key)
    modBits = Util.number.size(cipher._key.n)
    k = modBits/8 # Convert from bits to bytes
    print k
    return cipher.decrypt(ciphertext)

def encrypt_file(file_name, key):
    print 'Encrypt called'
    print key
    enc=b''
    fo=open(file_name,'rb')
    while True:
        plaintext = fo.read(64)
        print plaintext
        if len(plaintext)==0:
            break
        enc+=encrypt(plaintext, key)
    #print enc
    fo.close()
    overwrite=open(file_name,'wb')
    overwrite.write(enc)
    overwrite.close()
    # fo=open('E'+file_name.name.split("/")[-1], 'wb')
    # fo.write(enc)
    # fo.close()

def decrypt_file(file_name, key):
    file_name=path.normpath(file_name)
    pathway=getcwd()
    #print pathway
    dec=b''
    fo=open(pathway+file_name, 'rb')
    while True:
        ciphertext = fo.read(256)
        print 'LENGTH',
        print len(ciphertext)
        if len(ciphertext)==0:
            break

        if len(ciphertext)<256: #pad
            ciphertext=ciphertext+ b"\0" * (256 - len(ciphertext) % 256)
            print 'corrected',
            print len(ciphertext)
        dec+=decrypt(ciphertext, key)
    #print dec
    return dec

def filepath_handler(instance,name):
    return path.normpath(path.join('user_%d'%instance.posted_bulletin.author.id,'bulletin_%d'%instance.posted_bulletin.b_key,name))


# class Permission(models.Model):
#     p_key=models.AutoField(primary_key=True)
#     owner=models.ForeignKey(User,related_name='granter')
#     permitted=models.ForeignKey(User,related_name='granted')

class Key(models.Model):
    k_key=models.AutoField(primary_key=True)
    owner=models.ForeignKey(User)
    public=models.CharField(max_length=2048)

# Document Model
def keylookup(userobject):
    results=Key.objects.filter(owner__exact=userobject)
    for p in results:
        return p.public
class Document(models.Model):
    posted_bulletin=models.ForeignKey(Bulletin)
    docfile = models.FileField(upload_to=filepath_handler)
    d_key = models.AutoField(primary_key=True)
    # def save(self, *args, **kwargs):
    #     super(Document, self).save(*args, **kwargs)
    #     #print self.docfile.name
    #     snake=path.join(getcwd(),'media',self.docfile.name)
    #     # encrypt_file(snake,None)
    #     encrypt_file(snake,None)

    def save(self, encrypted=1,*args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        #print self.docfile.name
        snake=path.join(getcwd(),'media',self.docfile.name)
        if encrypted==1:
            encrypt_file(snake,keylookup(self.posted_bulletin.author))
        elif encrypted!=self.posted_bulletin.encrypted:
            if encrypted: #want to be encrypted, wasn't before
                print 'encrypting previously unencrypted'
                encrypt_file(snake,keylookup(self.posted_bulletin.author))
            else:
                print 'decrypted previously encrypted'
                guts=decrypt_file(snake,keylookup(self.posted_bulletin.author))
                filewrit=open(snake,'wb')
                filewrit.write(guts)
                filewrit.close()
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
