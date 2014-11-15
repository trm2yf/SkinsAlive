__author__ = 'Zachary'
from django.conf.urls import patterns, url

urlpatterns = patterns('sprint1.views',
    url(r'^list', 'list', name='list'),
    url(r'^bulletin', 'bulletin', name='bulletin'),
    url(r'^', 'home',name='home')
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    )
