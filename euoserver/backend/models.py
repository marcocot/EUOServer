import base64
import random
import string
import rsa
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


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