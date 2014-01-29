__author__ = 'Marco Cotrufo'

import logging
from time import time

logger = logging.getLogger(__name__)


class LoggingMiddleware(object):
    """ Middleware che effettua il loggin di ogni request
    """

    def process_request(self, request):
        request.timer = time()
        return None

    def process_response(self, request, response):
        logger.info('[%s] %s (%.1fs) REQUEST %s META %s',
            response.status_code,
            request.get_full_path(),
            time() - request.timer,
            request.REQUEST,
            self._save_meta(request)
        )
        return response

    def _save_meta(self, request):
        return [{k: request.META[k]} for k in request.META.keys() if k.startswith('SERVER') or k.startswith('HTTP')]