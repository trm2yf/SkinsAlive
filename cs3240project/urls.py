from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
#from django.views.generic import RedirectView

urlpatterns = patterns('',
    (r'^', include('sprint1.urls')),
#	(r'^$', RedirectView.as_view(url='/sprint1/list/')), # Just for ease of use.
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# urlpatterns = patterns('',
#     # Examples:
#     #url(r'^$', 'cs3240project.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     (r'^', include('sprint1.urls')),
#     url(r'^admin/', include(admin.site.urls)),
# )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
