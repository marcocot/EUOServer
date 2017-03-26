__author__ = 'marco'

from django.conf.urls import url
from .views import ScriptDetailView, GenerateClientView, ScriptView

urlpatterns = [
    url(r'^common/(?P<slug>.*)/$', ScriptView.as_view(), name='common'),
    url(r'^(?P<charid>.*)/(?P<slug>.*)/$', GenerateClientView.as_view(), name='generate'),
    url(r'^(?P<slug>.*)/$', ScriptDetailView.as_view(), name='view')
]
