__author__ = 'marco'

from django.conf.urls import patterns, url
from .views import ScriptDetailView

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', ScriptDetailView.as_view(), name='view')
)