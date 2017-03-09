__author__ = 'marco'

from django.conf.urls import url
from .views import ScriptDetailView

urlpatterns = [
    url(r'^(?P<slug>.*)/$', ScriptDetailView.as_view(), name='view')
]
