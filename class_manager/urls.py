from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from registration.views import register
from users.forms import CustomRegistrationForm
from users.views import user_home
from assignments.views import submit

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Examples:
    #url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^class_manager/', include('class_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^$', user_home, name='home'),

    url(r'^submit/$', submit, name='submit'),

    url(r'^register/$', register,
        {'backend': 'users.regbackend.CustomBackend',
         'form_class': CustomRegistrationForm},
        name='register'),

    # hack for after login redirect
    (r'^users/', redirect_to, {'url': '/'}),
)
