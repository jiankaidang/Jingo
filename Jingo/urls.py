from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Jingo.views.home', name='home'),
    # url(r'^Jingo/', include('Jingo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Jingo.views.index', name='index'),
    url(r'^admin/$', 'Jingo.views.admin', name='admin'),
    url(r'^pages/(?P<mode>\w+)/$', 'Jingo.views.pages', name='pages'),
    url(r'^tasks/(?P<mode>\w+)/$', 'Jingo.views.tasks', name='tasks'),
)
