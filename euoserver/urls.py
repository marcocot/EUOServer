from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^scripts/', include('euoserver.backend.urls', namespace='scripts')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   