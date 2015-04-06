from django.conf.urls import url

from lifting import views

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.month, name='lifting-month'),

    url(r'^fitnotes/$', views.fitnotes_upload),
]
