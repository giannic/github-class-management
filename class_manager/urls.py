from django.conf.urls import patterns, include, url
from registration.views import register
from users.forms import CustomRegistrationForm
from users.views import user_home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^class_manager/', include('class_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    (r'^$', user_home),
    url(r'^register/$', register,
        {'backend': 'users.regbackend.CustomBackend',
         'form_class': CustomRegistrationForm}),
)
