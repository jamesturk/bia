from django.conf.urls import url

from lifting import views

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.month_lifts,
        name='lifting-month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.day_lifts,
        name='lifting-day'),

    url(r'^fitnotes/$', views.fitnotes_upload),
]
