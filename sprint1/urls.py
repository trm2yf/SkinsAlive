__author__ = 'Zachary'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sprint1.views',
    url(r'^list', 'list', name='list'),
    url(r'^addbul', 'addbul', name='addbul'),
    url(r'^bulletin', 'bulletin', name='bulletin'),
    url(r'^folder', 'folder', name='folder'),
    url(r'^index', 'home',name='home'),
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^profile', 'profile', name='profile'),
    url(r'^logout', 'user_logout', name='logout'),
    url(r'^search', 'search', name='search'),
    url(r'^decrypt','decrypt',name='search'),
    url(r'^edit', 'edit', name='edit'),
    url(r'^copy', 'copy', name='copy'),
    url(r'^bdisplay', 'bdisplay', name='bdisplay'),

#    url(r'^admin', 'admin', name='admin')
    )
