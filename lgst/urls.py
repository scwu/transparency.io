from django.conf.urls import patterns, include, url
from django.conf import settings
from app import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'lgst.app.views.index', name='home'),
    url(r'^_request_data', 'lgst.app.views.get_results', name='search')
    # Examples:
    # url(r'^$', 'lgst.views.home', name='home'),
    # url(r'^lgst/', include('lgst.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
