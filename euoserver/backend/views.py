import logging
import base64
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import rsa
from .models import Script

logger = logging.getLogger(__name__)


class EUOViewMixin(object):
    def check_request(self, request):

        if not 'HTTP_X_KEY' in request.META:
            raise ValueError('Key non presente')

        if not 'HTTP_X_CHARID' in request.META:
            raise ValueError('CharId non presente')

        decrypted_char_id = rsa.decrypt(base64.urlsafe_b64decode(request.META['HTTP_X_KEY']), settings.PRIVATE_KEY)
        char_id = request.META['HTTP_X_CHARID']

        if decrypted_char_id != char_id:
            raise ValueError('La chiave pubblica non corrisponde con il charid')

        return decrypted_char_id


class ScriptDetailView(EUOViewMixin, View):
    """ Visualizza
    """

    model = Script
    http_method_names = ['post', ]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        try:
            self.char_id = self.check_request(request)
        except Exception:
            logger.exception("Impossibile determinare la request")
            self.char_id = None

        return super(ScriptDetailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        script = get_object_or_404(Script, hash__exact=self.kwargs['slug'])

        response = HttpResponse(content_type='text/x-euo')
        response['Content-Disposition'] = 'attachment; filename="%s.euo"' % slugify(script.title)

        if script.script:
            response.write(script.script.read())

        return response