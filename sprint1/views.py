from django.contrib.auth import authenticate
from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from sprint1.models import Document,Bulletin
from forms import DocumentForm,AccountForm,BulletinForm,UserForm
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User

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
def location_lookup(citystring):
    '''Implement string lookup to latitude and longitude here'''
    return (0,0)

def auth_util(passedrequest):

    if passedrequest.user.id==None:
        return 1
    else:
        return passedrequest.user.id

def bulletin(request):
    userid=auth_util(request)
    if userid<0:
        return render_to_response('login.html', {}, RequestContext(request))
    DocumentFormSet=formset_factory(DocumentForm,extra=2)
    if request.method == 'POST':
        form =BulletinForm(request.POST)
        if form.is_valid():
            print 'Saving Bulletin'
            print request.user
            lat,long=location_lookup(request.POST['location'])
            enc=1
            if request.POST['encrypted']!='on':
                enc=0
            bulletin = Bulletin(author_id=userid,title=request.POST['title'],lat=lat,long=long,text_description=request.POST['text_description'], encrypted=enc )
            bulletin.save()
        doc_formset=DocumentFormSet(request.POST,request.FILES,prefix='documents')
        if doc_formset.is_valid() and form.is_valid():
            for doc in doc_formset:
                print 'Saving a file'
                cd=doc.cleaned_data
                newdoc = Document(docfile=cd.get('docfile'),posted_bulletin=bulletin.b_key)
                newdoc.save()
        return HttpResponseRedirect(reverse('sprint1.views.bulletin'))
    else:
        form=BulletinForm()
        doc_formset=DocumentFormSet(prefix='documents')
    return render_to_response(
        'bulletin.html',{'form':form,'doc_formset':doc_formset},
        context_instance=RequestContext(request)
    )



def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
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

#Account Creation Function
def register(request):
    context = RequestContext(request)

    #initially this is set to be false and is updated if the user is registered
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        #If the form valid
        if user_form.is_valid():
            user = user_form.save()
            #the set_password method will hash the password
            user.set_password(user.password) #Django does this to password fields by default.
            user.save()

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


#Log-in Function
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        #If the password/username combination is valid, an User Object will be returned
        user = authenticate(username=username, password=password)

        if user:
            #check if the account is active and then redirect back to main page
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bulletin')
            else:
                #otherwise account is inactive
                return HttpResponse("Account is not active")
        else:
            #invalid username/password combination
            return HttpResponse("The username and password combination that you provided is invalid")

    else:
        #The request is not a POST so it's probably a GET request
        return render_to_response('login.html', {}, context)

#Search Function
def search(request):
    context = RequestContext(request)

    if request.method == 'POST':
        search_text = request.POST['search_text']
        search_type = request.POST['type']

        #Keyword Search Option
        if search_type == 'all':
            q1 = Bulletin.objects.filter(title__icontains=search_text)
           # q2 = q1.filter(Bulletin.objects.filter(text_description__icontains=search_text))
            #extra logic needed for dates?
           # q3 =q2.filter(Bulletin.objects.filter(date_created__icontains=search_text))
            query = q1.order_by('date_created', 'title')

        # Title Search Option
        if search_type == 'title':
            # if text is contained within title
            q1 = Bulletin.objects.filter(title__icontains=search_text)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')

        #Author Search Option
        if search_type == 'author':
            # if text is contained within title
            q1 = Bulletin.objects.filter(authors__icontains=search_text)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')

        if search_type == 'date':
            # if text is contained within title
            q1 = Bulletin.objects.filter(date_created__year=search_text)
            # order by publication date, then headline
            query =q1.order_by('date_created', 'title')




        bulletins = [b for b in query]
       # print string
        return render_to_response('search.html', {'bulletins':bulletins}, context)

    else:
        #The request is not a POST so it's probably a GET request
        return render_to_response('search.html', {}, context)


