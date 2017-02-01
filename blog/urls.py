from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^editor/', include(admin.site.urls)),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^', include('eminer.urls')),
)
