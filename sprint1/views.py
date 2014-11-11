from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sprint1.models import Document,Users,Bulletin
from sprint1.forms import DocumentForm,AccountForm,BulletinForm
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
    return 0,0
def bulletin(request):
    if request.method == 'POST':
        form =BulletinForm(request.POST)
        if form.is_valid():
            lat,long=location_lookup(request.location)
            bulletin = Bulletin(title=request.POST.title,lat=lat,long=long,text_description=request.POST.text_description, encrypted=request.POST.encrypted )
            bulletin.save()
            return HttpResponseRedirect(reverse('sprint1.views.bulletin'))
    else:
        form=BulletinForm()
    return render_to_response(
        'bulletin.html',{'form':form},
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
