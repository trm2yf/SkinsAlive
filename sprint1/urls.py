__author__ = 'Zachary'
from django.conf.urls import patterns, url

urlpatterns = patterns('sprint1.views',
    url(r'^list', 'list', name='list'),
    url(r'^bulletin', 'bulletin', name='bulletin'),
    url(r'^index', 'home',name='home'),
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'user_login', name='login'),
    )
