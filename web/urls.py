from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^fitnotes-upload/$', 'lifting.views.fitnotes_upload'),
    url(r'^lifting/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'lifting.views.month'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
