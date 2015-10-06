from django.conf.urls import include, url
from django.contrib import admin
from webportal.apps.main import urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(urls))
]

urlpatterns += staticfiles_urlpatterns()
