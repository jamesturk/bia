from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

import lifting.urls
import profiles.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include(profiles.urls.urlpatterns)),
    url(r'^lifting/', include(lifting.urls.urlpatterns)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
