import logging
import base64

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import rsa

from .models import Script, Ban, Access, Char

logger = logging.getLogger(__name__)


class EUOViewMixin(object):
    def check_request(self, request):
        """ Verifica che la richiesta sia effettivamente valida
        """

        # Prima di tutto verifichiamo che non esistano ban attivi
        check = Ban.objects.filter(ip=Ban.get_client_ip(request), expires__gte=now()).first()

        if check:
            logger.warning("Tentativo di accesso da parte di un ip bannato: %r. Scadenza ban: %s", check.ip,
                           check.expires)
            raise PermissionDenied('IP Bannato')

        if not 'HTTP_X_KEY' in request.META:
            logger.warning("Non e' stata passata la chiave pubblica")
            raise PermissionDenied('Key non presente')

        if not 'HTTP_X_CHARID' in request.META:
            logger.warning("Non e' stato passato il charid")
            raise PermissionDenied('CharId non presente')

        if not 'SERVER_PROTOCOL' in request.META or request.META['SERVER_PROTOCOL'] != 'HTTP/1.0':
            logger.warning("Il server protocol non corrisponde")
            raise PermissionDenied('Server protocol non valido')

        try:
            decrypted_char_id = rsa.decrypt(base64.urlsafe_b64decode(request.META['HTTP_X_KEY']), settings.PRIVATE_KEY)
            char_id = request.META['HTTP_X_CHARID']

            if decrypted_char_id != char_id:
                logger.warning("La chiave pubblica non corrisponde con il charid: cid %s chiave %s", char_id,
                               decrypted_char_id)
                raise PermissionDenied('La chiave pubblica non corrisponde con il charid')

            return decrypted_char_id
        except TypeError:
            logger.exception('Errore di decodifica del base64')
            raise ValueError()


class ScriptDetailView(EUOViewMixin, View):
    """ Restituisce al client il contenuto di uno script
    """

    model = Script
    http_method_names = ['post', ]
    char_id = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        try:
            self.char_id = self.check_request(request)
        except ValueError:
            logger.exception("Impossibile determinare la request")
            self.char_id = None
        except PermissionDenied:
            logger.info("Creo un nuovo ban per la request")
            Ban.create_from_request(request)
            raise

        return super(ScriptDetailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        logger.info("Richiesto lo script %s", self.kwargs['slug'])

        script = get_object_or_404(Script, hash__exact=self.kwargs['slug'])
        char = get_object_or_404(Char, char_id__exact=self.char_id)

        if not Access.objects.has_access(char=char, script=script):
            logger.warn("L'utente ha richiesto uno script a cui non ha accesso: %s - %s", char, script)
            raise PermissionDenied("Accesso non consentito")

        response = HttpResponse(content_type='text/x-euo')
        response['Content-Disposition'] = 'attachment; filename="%s.euo"' % slugify(script.title)

        if script.script:
            response.write(script.script.read())

        logger.info("Accesso consentito allo script: %s, char: %s", script, char)
        return response
