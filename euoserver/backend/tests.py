from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.test import TestCase
from autofixture import AutoFixture
from .models import Script, Char, Ban


class ScriptViewTestCase(TestCase):
    def setUp(self):
        self.script = AutoFixture(Script).create_one()

    def _action(self, url_name, url_args=None, method='get', **headers):
        url = reverse(url_name, kwargs=url_args or {})

        if not hasattr(self.client, method):
            raise Exception('Metodo non valido ' + method)

        fn = getattr(self.client, method)
        return fn(url, **headers)

    def test_view_should_accept_only_post_requests(self):
        for method in ['get', 'put', 'patch', 'delete', 'head', 'options']:
            response = self._action('scripts:view', {'slug': self.script.hash}, method, HTTP_X_KEY='KEY',
                HTTP_X_CHARID='CHARID')
            self.assertEqual(405, response.status_code)

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', HTTP_X_KEY='KEY',
            HTTP_X_CHARID='CHARID')
        self.assertEqual(200, response.status_code)

    def test_view_should_check_for_banned_ip(self):
        """ Se un indirizzo e' stato bannato non deve poter accedere agli script
        """

        ban = Ban.objects.create(ip='0.0.0.0')
        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', HTTP_X_FORWARDED_FOR=ban.ip)

        self.assertEquals(403, response.status_code)

    def test_view_should_create_ban_for_invalid_request(self):
        """ Quando la richiesta non e' validata procediamo alla creazione del ban
        """

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', HTTP_X_FORWARDED_FOR='1.1.1.1')

        self.assertEquals(403, response.status_code)
        self.assertTrue(Ban.objects.filter(ip='1.1.1.1', expires__gt=now()).exists())


class ScriptModelTestCase(TestCase):
    def test_compute_hash_on_save(self):
        script = Script()
        script.save()

        self.assertIsNotNone(script.hash, "Non e' stato generato l'hash per lo script")


class BanModelTestCase(TestCase):
    def test_compute_default_expire_date(self):
        """ Quando si crea un nuovo ban automaticamente deve calcolare la data di scadenza
        """

        ban = Ban(ip='0.0.0.0')
        ban.save()

        self.assertGreater(ban.expires, now())


class CharModelTestCase(TestCase):
    def test_compute_public_key_on_create(self):
        """ Quando si genera un nuovo char deve essere creata la public key
        """

        char = Char.objects.create(name='Char', shard='Shard', char_id='CharId')

        self.assertIsNotNone(char.public_key, 'La chiave non e\' stata generata')