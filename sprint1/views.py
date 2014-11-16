from django.contrib.auth import authenticate
from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from sprint1.models import Document,Users,Bulletin
from sprint1.forms import DocumentForm,AccountForm,BulletinForm,UserForm
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login

def home(request):
    if request.method == 'POST':
        form =AccountForm(request.POST)
        if form.is_valid():
            user = Users(u_name=request.POST.username,email=request.POST.email,password=request.POST.password)
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
def bulletin(request):
    DocumentFormSet=formset_factory(DocumentForm,extra=2)
    if request.method == 'POST':
        form =BulletinForm(request.POST)
        if form.is_valid():
            lat,long=location_lookup(request.location)
            bulletin = Bulletin(title=request.POST.title,lat=lat,long=long,text_description=request.POST.text_description, encrypted=request.POST.encrypted )
            bulletin.save()
        doc_formset=DocumentFormSet(request.POST,request.FILES,prefix='documents')
        if doc_formset.is_valid():
            for doc in doc_formset:
                cd=doc.cleaned_data
                newdoc = Document(docfile=cd.get('docfile'))
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
            #user.set_password(user.password) Django does this to password fields by default.
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
                return HttpResponseRedirect('/index/')
            else:
                #otherwise account is inactive
                return HttpResponse("Account is not active")
        else:
            #invalid username/password combination
            return HttpResponse("The username and password combination that you provided is invalid")

    else:
        #The request is not a POST so it's probably a GET request
        return render_to_response('login.html', {}, context)




