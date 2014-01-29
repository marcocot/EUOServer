import base64
import random
import string
import datetime

import rsa
from django.conf import settings
from django.utils.timezone import now
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import AccessManager


class Char(models.Model):
    """ Singolo personaggio
    """

    name = models.CharField(max_length=80, verbose_name=_('name'))
    shard = models.CharField(max_length=120, verbose_name=_('shard'))
    char_id = models.CharField(max_length=6, verbose_name=_('char id'))
    public_key = models.CharField(max_length=200, verbose_name=_('public key'), blank=True, null=True)

    class Meta:
        verbose_name = _('char')
        verbose_name_plural = _('chars')

    def save(self, *args, **kwargs):
        if not self.public_key:
            # Bisogna fare attenzione che rsa.encrypt funziona sono con stringhe ascii
            self.public_key = base64.urlsafe_b64encode(rsa.encrypt(self.char_id.encode('ascii'), settings.PUBLIC_KEY))

        super(Char, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.shard)


class Script(models.Model):
    """ Script
    """

    title = models.CharField(max_length=120, verbose_name=_('name'))
    hash = models.CharField(max_length=12, verbose_name=_('hash'), blank=True, null=True, editable=False)
    script = models.FileField(verbose_name=_('script'), upload_to='scripts')

    class Meta:
        verbose_name = _('script')
        verbose_name_plural = _('scripts')

    def save(self, *args, **kwargs):
        if not self.pk or not self.hash:
            self.hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(12))

        super(Script, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Ban(models.Model):
    """ Rappresenta un ban temporaneo ad un indirizzo IP
    """

    DEFAULT_TIME = datetime.timedelta(days=1)

    ip = models.IPAddressField(verbose_name=_('ip address'))
    expires = models.DateTimeField(verbose_name=_('date of expire'), blank=True, null=True)

    class Meta:
        verbose_name = _('ban')
        verbose_name_plural = _('bans')

    @classmethod
    def get_client_ip(cls, request):
        """ Restituisce l'indirizzo ip del client
        """

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def create_from_request(cls, request):
        """ Crea un nuovo ban dalla request
        """

        ip = cls.get_client_ip(request)

        if Ban.objects.filter(ip=ip, expires__gte=now()).exists():
            ban = Ban.objects.filter(ip=ip).first()

            # Impostando a none l'expires verra' automaticamente calcolato nel save
            ban.expires = None
        else:
            ban = Ban.objects.create(ip=ip)

        ban.save()

    def save(self, *args, **kwargs):
        """ Quando si salva imposta a automaticamente l'expire
        """

        if not self.expires:
            self.expires = now() + self.DEFAULT_TIME

        super(Ban, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{}x{}".format(self.ip, self.expires)


class Access(models.Model):
    """ Accesso di un char specifico ad uno script
    """

    char = models.ForeignKey('backend.Char', verbose_name=_('char'))
    script = models.ForeignKey('backend.Script', verbose_name=_('script'))
    expire = models.DateField(verbose_name=_('date of expire'), blank=True, null=True)

    objects = AccessManager()

    class Meta:
        verbose_name = _('script access')
        verbose_name_plural = _('script accesses')
        unique_together = ['char', 'script']

    def __unicode__(self):
        return u"{} -> {}".format(self.char, self.script)