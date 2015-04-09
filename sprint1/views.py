from django.contrib.auth import authenticate
from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from sprint1.models import Document,Skin,Folder,Key,Author,Request

from sprint1.forms import DocumentForm,AccountForm,SkinForm,UserForm,FolderForm,SForm,AddBulForm

from sprint1.forms import DocumentForm,AccountForm,BulletinForm,UserForm,FolderForm,BulForm,AddBulForm

from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import construct
from django.contrib.auth.decorators import login_required
import random
import datetime
from django.db.models import F,Q
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim,GoogleV3
from geopy import units
def home(request):
    if request.method == 'POST':
        form =AccountForm(request.POST)
        if form.is_valid():
            user = User(username=request.POST.username,email=request.POST.email,password=request.POST.password)
            user.save()
            return HttpResponseRedirect(reverse('sprint1.views.home'))
    else:
        form=AccountForm()
        return render_to_response(
        'index.html',{'form':form},
        context_instance=RequestContext(request)
    )
#Goes with the AddBulForm form; this will associate the bulletin with the folder by updating the folder field of the bulletin to be that of the folder
def addbul(request):
    context = RequestContext(request)
    author = request.user.id
    folders=None
    if request.method == 'POST':

        # retrieves all bulletins of the current viewer
        q1 = Skin.objects.filter(author__exact=author)
        bulletins = [b for b in q1]

        # retrieves all folders of the current viewer
        q2 = Folder.objects.filter(owner__exact=author)

        folders = [f for f in q2]
        return render_to_response('addbul.html',{'folder':folders,'bulletin':bulletins}, context)
    else:
        # retrieves all bulletins of the current viewer
        q1 = Skin.objects.filter(author__exact=author)
        bulletins = [b for b in q1]

        # retrieves all folders of the current viewer
        q2 = Folder.objects.filter(owner__exact=author)

        return render_to_response('addbul.html',{'folder':folders, 'bulletin':bulletins}, context)

#Goes with the AddBulForm form; this will associate the bulletin with the folder by updating the folder field of the bulletin to be that of the folder
def connect(request):
    userid=auth_util(request)
    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    if request.method == 'POST':
        print form.is_valid()
        if form.is_valid():
            print 'Adding bulletin to folder'
            bulletin = request.POST['bulletinval']
            bulletin.folder = models.ForeignKey(request.POST['folderval'])
            bulletin.save(update_fields=['folder'])
        return HttpResponseRedirect(reverse('sprint1.views.addbul'))
    else:
       return HttpResponseRedirect(reverse('sprint1.views.addbul'))



def location_lookup(citystring):
    try:

        #geolocator = Nominatim()
        geolocator=GoogleV3()
        location = geolocator.geocode(citystring)
        return(location.latitude, location.longitude)
    except:
    #'''Implement string lookup to latitude and longitude here'''
        return (0,0)

def auth_util(passedrequest):

    if passedrequest.user.id==None:
        return 1
    else:
        return passedrequest.user.id

def folder(request):
    userid=auth_util(request)
    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    if request.method == 'POST':
        form =FolderForm(request.POST)
        b1 = request.POST['test']
        b2 = request.POST['test1']
        b3 = request.POST['test2']

        print form.is_valid()
        if form.is_valid():
            print 'Saving Folder'
            print request.user
            folder = Folder(owner=request.user,name=request.POST['name'])
            folder.save()
            f_id = folder.f_key

        Skin.objects.filter(b_key=b1).update(folder_id=f_id)
        Skin.objects.filter(b_key=b2).update(folder_id=f_id)
        Skin.objects.filter(b_key=b3).update(folder_id=f_id)

        return HttpResponseRedirect('/profile')
    else:
        form=FolderForm()
        q1 = Skin.objects.filter(author__exact=userid)
        bulletins = [b for b in q1]
        return render_to_response(
            'folder.html',{'form':form, 'bulletins':bulletins},
            context_instance=RequestContext(request)
        )

def requestskin(request):
	userid=auth_util(request)

	if userid<0:
		return render_to_response('login.html', {}, RequestContext(request))	
	form=RequestForm()
	if request.method=='POST':
		form = RequestForm(request.POST, request.FILES)
		if form.is_valid():
			print form.is_valid()
			req = Request(owner=request.user,text_description=request.POST['text_description'])
			if request.FILES:
				req.imgfile=request.FILES['imgfile']
			else:
				req.imgfile=NULL
			req.save()
		return HttpResponseRedirect('/profile')
	return render_to_response('request.html', {'form':form},context_instance=RequestContext(request))

def bulletin(request):
    userid=auth_util(request)

    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    DocumentFormSet=formset_factory(DocumentForm,extra=2)
    form =SkinForm(request.user)

    if request.method == 'POST':
        form = SkinForm(request.user, request.POST)

        print form.is_valid()
        if form.is_valid():
            print 'Saving Skin'
            print request.user
            lat,long=location_lookup(request.POST['location'])
            enc=1
            try:
                request.POST['encrypted']=='on'
                enc=1
            except:
                enc=0
                pass
            bulletin = Skin(folder=Folder.objects.filter(f_key__exact=request.POST['folder'])[0],author_id=userid,title=request.POST['title'],text_description=request.POST['text_description'])
            bulletin.save()
        doc_formset=DocumentFormSet(request.POST,request.FILES,prefix='documents')
        if doc_formset.is_valid() and form.is_valid():
            for doc in doc_formset:
                print 'Saving a file'
                cd=doc.cleaned_data
                if cd.get('docfile')!=None:
                    newdoc = Document(docfile=cd.get('docfile'),posted_bulletin=bulletin)
                    newdoc.save()
        return HttpResponseRedirect('/profile')
    else:
        doc_formset=DocumentFormSet(prefix='documents')
    return render_to_response(
        'bulletin.html',{'form':form,'doc_formset':doc_formset},
        context_instance=RequestContext(request)
    )

# def grant(request):
#     userid=auth_util(request)
#     if userid<0:
#         return render_to_response('login.html', {}, RequestContext(request))
#     context = RequestContext(request)
#     completed=None
#     if request.method=='POST':
#         form=PermissionForm(request.POST,request.FILES)

#         if form.is_valid():
#             grantee=[i for i in User.objects.filter(id__exact=request.POST['permitted'])][0]
#             owner=[i for i in User.objects.filter(id__exact=request.user.id)][0]
#             perm=Permission(owner=owner,permitted=grantee)
#             perm.save()
#             completed=True
#             file=request.FILES['private']
#             for pub in Key.objects.filter(owner__exact=request.user):
#                 load=pub.public
#                 # key=RSA.importKey(load,None)
#                 # cipher = PKCS1_OAEP.new(key)
#                 # pkey=construct((cipher._key.n,cipher._key.e,long(random.randint(1,10))))


#                 from django.core.mail import send_mail,EmailMessage
#                 print 'sending email?'
#                 mail = EmailMessage('SecureWitness', 'Do not lose the enclosed file. Do not reply. Access to '+request.user.username+'\'s encrypted bulletins', ('Secure Witness','3240project@gmail.com'), (grantee.username,grantee.email))
#                 mail.attach('private.pem',file.read())
#                 mail.send()
#     else:
#         form = PermissionForm()
#     return render_to_response('permission.html',{'form':form,'completed':completed},context)

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'],posted_bulletin=None)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('sprint1.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
# Create your views here.
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5

# Use a larger key length in practice...
KEY_LENGTH = 2048  # Key size (in bits)
random_gen = Random.new().read

# Generate RSA private/public key pairs for both parties...

def register(request):
    context = RequestContext(request)

    #initially this is set to be false and is updated if the user is registered
    registered = False
    pkey=None
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)


        #If the form valid
        if user_form.is_valid():
            user = user_form.save()
            #the set_password method will hash the password
            user.set_password(user.password) #Django does this to password fields by default.
            user.save()
            # #is_author = request.POST['author']
            # #if is_author != u'on' :
            if 'author' in request.POST:
                author = Author(user_id=user)
                author.save()

            # pubkey=RSA.generate(KEY_LENGTH,random_gen)
            # key = Key(owner=user,public=pubkey.publickey().exportKey('PEM'))
            # key.save()
            # pkey=pubkey.exportKey('PEM')

            # # if 'author' in request.POST:
            #     from django.core.mail import send_mail,EmailMessage
            #     mail = EmailMessage('SecureWitness', 'Do not lose the enclosed file. Do not reply.', ('Secure Witness','3240project@gmail.com'), (user.username,user.email))
            #     mail.attach('private.pem',pkey)
            #     mail.send()
            # # except Exception as e:
            # #     print e
            #     perm=Permission(owner=user,permitted=user)
            #     perm.save()
            folder=Folder(owner=user,name='Default')
            folder.save()
            #update the registered variable to be true
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render_to_response(
        'register.html',
        {'user_form': user_form, 'registered':registered},
        context)
        
#function to check if user is author
def is_author(userid):
    if Author.objects.filter(user_id=userid).count():
        return True

    return False

#Log-in Function
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        #If the password/username combination is valid, an User Object will be returned
        user = authenticate(username=username, password=password)
        # profile = request.user.get_profile()

        if user:
            #check if the account is active and then redirect back to main page
            if user.is_active:
                login(request, user)
               # if profile.author: 
 #                  if User.objects.filter(username=username).count():
                if is_author(user):
                    return HttpResponseRedirect('/profile')
                else:
                    return HttpResponseRedirect('/frontpage')
              #  else:
                #    return HttpResponseRedirect('/index')
            else:
                #otherwise account is inactive
                return HttpResponse("Account is not active")
        else:
            #invalid username/password combination
            return HttpResponse("The username and password combination that you provided is invalid")

    else:
        #The request is not a POST so it's probably a GET request
        return render_to_response('login.html', {}, context)

#logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/index/')



#Search Function
def search(request):
    context = RequestContext(request)

    if request.method == 'POST':
        search_text = request.POST['search_text']
        search_type = request.POST['type']
        granted=Permission.objects.filter(permitted__exact=request.user)
        granted=[i.owner for i in granted]

        #Keyword Search Option
        if search_type == 'all':

            q1 = Skin.objects.filter(
    Q(title__icontains=search_text) |
    Q(text_description__icontains=search_text))


            query = q1.order_by('date_created', 'title')

        # Title Search Option
        if search_type == 'title':
            # if text is contained within title
            q1 = Skin.objects.filter(title__icontains=search_text)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')

        #Author Search Option
        if search_type == 'author':
            # gets author id based on search of username
            author = User.objects.get(username__exact=search_text)

            id = author.id
            # query db to find all bulletins with given id
            q1 = Skin.objects.filter(author_id__exact=id)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')

        if search_type == 'date':
            # if text is contained within title
            q1 = Skin.objects.filter(date_created=search_text)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')

        #if search_type =='location':
        #    lat,long=location_lookup(search_text)
        #    rough_distance = units.degrees(arcminutes=units.nautical(miles=50))
        #    q1=Skin.objects.filter(Q(lat__range=(lat-rough_distance,lat+rough_distance))|Q(long__range=(long-rough_distance,long+rough_distance)))
        #    query=q1.order_by('date_created','title')


        bulletins=[]
        for b in query:
           # if b.author in granted:
                bulletins.append(b)
       # # print string
       #  print "bulletins"
       #  print bulletins
        return render_to_response('search.html', {'bulletins':bulletins}, context)

    else:
        #The request is not a POST so it's probably a GET request
        return render_to_response('search.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
def user_logout(request):
    logout(request)

        # Take the user back to the homepage.
    return HttpResponseRedirect('/index')

def profile(request):
    context = RequestContext(request)
    author = request.user.id
    if is_author(author):

        if request.method == 'POST':
            delete = request.POST['delete']
            Skin.objects.filter(b_key=delete).delete()

            q1 = Skin.objects.filter(author__exact=author)

            bulletins = [b for b in q1]
            return render_to_response('profile.html', {'bulletins':bulletins}, context)
        else:
            q1 = Skin.objects.filter(author__exact=author)
            q2 = Folder.objects.filter(owner__exact=author)

            bulletins = [b for b in q1]
            folders = [f for f in q2]
            return render_to_response('profile.html', {'bulletins':bulletins, 'folders':folders}, context)

    else:
        return HttpResponseRedirect('/frontpage')


def readerprofile(request):
    context = RequestContext(request)
    author = request.user.id

    if request.method == 'POST':

        q1 = Skin.objects.filter(author__exact=author)

        bulletins = [b for b in q1]
        return render_to_response('readerprofile.html', {'bulletins':bulletins}, context)

    else:
        q1 = Skin.objects.filter(author__exact=author)

        bulletins = [b for b in q1]
        return render_to_response('readerprofile.html', {'bulletins':bulletins}, context)


def bdisplay(request):

    context = RequestContext(request)
    if request.method == 'POST':
        bulletin_key = request.POST['button_id']
        q1 = Skin.objects.filter(b_key__exact=bulletin_key)
      #  q2 = Skin.objects.filter(b_key__exact=bulletin_key)
        q1.update(num_views=F('num_views') + 1)
      #  q2.update(num_views=F('num_views') + 1)

        bulletin_enc = [b for b in q1]
       # bulletin_not = [c for c in q2]
        documents = Document.objects.filter(posted_bulletin_id__exact=bulletin_key)
        print 'DOCUMENT LENGTH',
        print len(documents)

        return render_to_response('bdisplay.html', {'bulletin_enc':bulletin_enc,'documents': documents}, context)

    else:
        return HttpResponseRedirect('/search')

def decrypt(request):
    reqdoc=request.POST['document']
    context=RequestContext(request)
    try:
        pkey=request.FILES['private']
        print 'uploaded'
        from models import decrypt_file
        bcontents=decrypt_file(reqdoc,pkey.read())
        response=HttpResponse(content_type='multipart/encrypted')
        response['Content-Disposition'] = 'attachment; filename='+reqdoc.split('/')[-1]
        response.write(bcontents)
        return response
    except Exception as e:
        print e
        print 'empty'
        return render_to_response('decrypt.html',{'document':reqdoc}, context)
        # return HttpResponseRedirect('/search')


def edit(request):
    context = RequestContext(request)
    author = request.user.id
    form =SkinForm(request.user)

    if request.method == 'GET':
        b_id = request.GET['edit']
        q1 = Skin.objects.filter(b_key=b_id, author__exact=author)
        bulletin = [b for b in q1]

        form=SkinForm(request.user, initial={'title': bulletin[0].title,
                                   'text_description': bulletin[0].text_description,

                                   'folder': bulletin[0].folder})
        return render_to_response(

        'edit.html',{'b_id':b_id,'form':form},
        context_instance=RequestContext(request)
        )

    else:
        form = SkinForm(request.user,request.POST)
        print form.is_valid()
        if form.is_valid():
            lat,long=location_lookup(request.POST['location'])
            enc=1
            try:
                request.POST['encrypted']=='on'
                enc=1
            except:
                enc=0
                pass
            bulletin=Skin.objects.filter(b_key__exact=request.POST['submit'])[0]
            bulletin.folder=Folder.objects.filter(f_key__exact=request.POST['folder'])[0]
            bulletin.author=request.user
            bulletin.title=request.POST['title']
            bulletin.text_description=request.POST['text_description']
            bulletin.save()
            docs=Document.objects.filter(posted_bulletin=bulletin)
            for doc in docs:
                doc.save()


        return HttpResponseRedirect('/profile')

def f_edit(request):
    context = RequestContext(request)
    author = request.user.id

    if request.method == 'GET':
        f_id = request.GET['f_edit']
        q1 = Folder.objects.filter(f_key=f_id, owner__exact=author)
        folder = [f for f in q1]

        form=FolderForm(initial={'name': folder[0].name})
        return render_to_response(
        'f_edit.html',{'f_id':f_id,'form':form},
        context_instance=RequestContext(request)
        )

    else:
        form = FolderForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            folder = Folder(owner=request.user,f_key=request.POST['submit'],name=request.POST['name'])
            folder.save()

        return HttpResponseRedirect('/profile')



def copy(request):
    context = RequestContext(request)
    author = request.user.id
    userid=auth_util(request)
    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    DocumentFormSet=formset_factory(DocumentForm,extra=2)
    if request.method == 'POST':
        form =SkinForm(request.user, request.POST)
        print form.is_valid()
        if form.is_valid():
            print 'Saving Skin'
            print request.user
            lat,long=location_lookup(request.POST['location'])
            enc=1
            try:
                request.POST['encrypted']=='on'
                enc=1
            except:
                enc=0
                pass
            bulletin = Skin(folder=Folder.objects.filter(f_key__exact=request.POST['folder'])[0],author_id=userid,title=request.POST['title'],text_description=request.POST['text_description'], encrypted=enc )
            bulletin.save()
        doc_formset=DocumentFormSet(request.POST,request.FILES,prefix='documents')
        if doc_formset.is_valid() and form.is_valid():
            for doc in doc_formset:
                #print 'Saving a file'
                cd=doc.cleaned_data
                if cd.get('docfile')!=None:
                    newdoc = Document(docfile=cd.get('docfile'),posted_bulletin=bulletin)
                    newdoc.save()
        return HttpResponseRedirect('/profile')
    else:
        b_id = request.GET['copy']
        query = Skin.objects.filter(b_key=b_id)
        bulletin = [b for b in query]

        form=SkinForm(request.user, initial={'title': bulletin[0].title,
                                   'text_description': bulletin[0].text_description,
                                   'folder': bulletin[0].folder})
        doc_formset=DocumentFormSet(prefix='documents')
        return render_to_response(
        'copy.html',{'form':form,'doc_formset':doc_formset},
        context_instance=RequestContext(request)
        )

def f_copy(request):
    userid=auth_util(request)
    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    BulFormSet=formset_factory(SForm,extra=3)
    if request.method == 'POST':
        form =FolderForm(request.POST)
        b1 = request.POST['test']
        b2 = request.POST['test1']
        b3 = request.POST['test2']

        print form.is_valid()
        if form.is_valid():
            print 'Saving Folder'
            print request.user
            folder = Folder(owner=request.user,name=request.POST['name'])
            folder.save()
            f_id = folder.f_key

        Skin.objects.filter(b_key=b1).update(folder_id=f_id)
        Skin.objects.filter(b_key=b2).update(folder_id=f_id)
        Skin.objects.filter(b_key=b3).update(folder_id=f_id)

        return HttpResponseRedirect('/profile')
    else:
        f_id = request.GET['f_copy']
        query = Folder.objects.filter(f_key=f_id)
        folder = [f for f in query]

        form=FolderForm(initial={'name': folder[0].name})

        q1 = Skin.objects.filter(author__exact=userid)
        bulletins = [b for b in q1]
        return render_to_response(
            'folder.html',{'form':form, 'bulletins':bulletins},
            context_instance=RequestContext(request)
        )

def deletefolder(request):
    context = RequestContext(request)
    author = request.user.id

    f_id = request.POST['delete']
    Folder.objects.filter(f_key=f_id).delete()
    Skin.objects.filter(folder_id=f_id).delete()

    return HttpResponseRedirect('/profile')

def frontpage(request):
    context = RequestContext(request)

    if request.method == 'POST':
        #search_text = request.POST['search_text']
        #search_type = request.POST['type']
        #granted=Permission.objects.filter(permitted__exact=request.user)
        #granted=[i.owner for i in granted]
        today = datetime.date.today()
        q1 = Skin.objects.filter(date_created__gte=today - timedelta(days=7))
            # order by publication date, then headline
        query1 =q1.order_by('-date_created', 'title')

        q2 = Skin.objects.all()
        query2 = q2.order_by('-num_views', 'title')
        recent_bulletins=[]

        for b1 in query1:
                recent_bulletins.append(b1)

        most_viewed_bulletins=[]
        for b2 in query2:
                most_viewed_bulletins.append(b2)
       # print string
        print "rec bulletins"
        print recent_bulletins
        print "viewed bulletins"
        print most_viewed_bulletins

        return render_to_response('frontpage.html', {'recent_bulletins':recent_bulletins,'most_viewed_bulletins':most_viewed_bulletins}, context)

    else:
        today = datetime.date.today()
        q1 = Skin.objects.filter(date_created__gte=today - timedelta(days=7))
            # order by publication date, then headline
        query1 =q1.order_by('-date_created', 'title')

        q2 = Skin.objects.all()
        query2 = q2.order_by('-num_views', 'title')
        recent_bulletins=[]

        for b1 in query1:
                recent_bulletins.append(b1)

        most_viewed_bulletins=[]
        for b2 in query2:
                most_viewed_bulletins.append(b2)
       # print string
        print "rec bulletins"
        print recent_bulletins

        print "viewed bulletins"
        print most_viewed_bulletins
        return render_to_response('frontpage.html', {'recent_bulletins':recent_bulletins,'most_viewed_bulletins':most_viewed_bulletins}, context)

def viewfolder(request):
    context = RequestContext(request)
    if request.method == 'POST':
        f_id = request.POST['f_id']
        q1 = Skin.objects.filter(folder_id__exact=f_id)

        bulletin = [b for b in q1]

        return render_to_response('viewfolder.html', {'bulletin':bulletin}, context)

    else:
        return HttpResponseRedirect('/profile')

