__author__ = 'Zachary'
from django.conf.urls import patterns, url

urlpatterns = patterns('sprint1.views',
    url(r'^list', 'list', name='list'),
)