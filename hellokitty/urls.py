from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from hellokitty.apps.torrentkitty import views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', views.home, name='home'),
                       url(r'^export$', views.export, name='export'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^$', include(admin.site.urls)),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT}),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),

                       )
