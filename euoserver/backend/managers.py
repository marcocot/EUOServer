__author__ = 'Marco Cotrufo'

from django.db import models
from django.db.models import Q
from django.utils.timezone import now


class AccessManager(models.Manager):
    def has_access(self, char, script):
        """ Verifica che un determinato char abbia accesso o meno ad uno script
        """

        return self.filter(Q(expire=None) | Q(expire__gte=now()), char=char, script=script).exists()