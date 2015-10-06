from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'webportal.apps.main.views.index'),
]
