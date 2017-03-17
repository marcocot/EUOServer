import datetime
import codecs
from autofixture import AutoFixture
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from euoserver.backend.models import Script, Ban, Char, Access
from .utils import encrypt, decrypt

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

    def test_create_from_request_should_check_for_duplicates(self):
        """ Se esiste gia' un ban **attivo** non ne creiamo un secondo, ma semplicemente lo estendiamo
        """

        request = HttpRequest()
        ban = Ban.objects.create(ip='0.0.0.0', expires=now() + datetime.timedelta(hours=1))

        # Proviamo a creare un secondo ban
        request.META['HTTP_X_FORWARDED_FOR'] = ban.ip

        Ban.create_from_request(request)

        from_db = Ban.objects.get(pk=ban.pk)

        # a questo punto deve essere stato esteso il ban
        self.assertGreater(from_db.expires, now() + datetime.timedelta(hours=2))

    def test_create_from_request_should_create_a_new_one_if_all_expired(self):
        """ Se tutti i ban sullo stesso ip sono gia' passati allora semplicemente ne creiamo uno nuovo
        """

        request = HttpRequest()
        ban = Ban.objects.create(ip='0.0.0.0', expires=now() - datetime.timedelta(hours=2))

        # Proviamo a creare un secondo ban
        request.META['HTTP_X_FORWARDED_FOR'] = ban.ip

        Ban.create_from_request(request)

        check = Ban.objects.filter(ip=ban.ip, expires__gt=now()).exclude(pk=ban.pk).exists()
        self.assertTrue(check)


class CharModelTestCase(TestCase):
    def test_compute_public_key_on_create(self):
        """ Quando si genera un nuovo char deve essere creata la public key
        """

        char = Char.objects.create(name='Char', shard='Shard', char_id='CharId')

        self.assertIsNotNone(char.public_key, 'La chiave non e\' stata generata')


class AccessModelTestCase(TestCase):
    def setUp(self):
        self.char = AutoFixture(Char).create_one()
        self.script = AutoFixture(Script).create_one()

        self.tomorrow = now() + datetime.timedelta(days=1)
        self.yesterday = now() - datetime.timedelta(days=1)

    def test_has_access_if_no_expire_set(self):
        Access.objects.create(char=self.char, script=self.script)
        self.assertTrue(Access.objects.has_access(self.char, self.script))

    def test_has_access_with_future_expire_date(self):
        Access.objects.create(char=self.char, script=self.script, expire=self.tomorrow)
        self.assertTrue(Access.objects.has_access(self.char, self.script))

    def test_has_access_with_expired_date(self):
        Access.objects.create(char=self.char, script=self.script, expire=self.yesterday)
        self.assertFalse(Access.objects.has_access(self.char, self.script))


class ScriptViewTestCase(TestCase):
    valid_headers = {'HTTP_X_KEY': None, 'HTTP_X_CHARID': None}

    def setUp(self):
        self.char = AutoFixture(Char, field_values={'public_key': None}).create_one()
        self.script = AutoFixture(Script).create_one()

        self.valid_headers['HTTP_X_KEY'] = self.char.public_key
        self.valid_headers['HTTP_X_CHARID'] = self.char.char_id
        self.valid_headers['SERVER_PROTOCOL'] = 'HTTP/1.0'
        self.valid_headers['HTTP_X_FORWARDED_FOR'] = '2.2.2.2'
        self.valid_headers['HTTP_X_RANDOM_ID'] = codecs.encode(self.script.hash, 'rot_13')
        self.valid_headers['HTTP_X_SHARD'] = self.char.shard
        self.valid_headers['HTTP_X_DECODE'] = self.char.name

    def _action(self, url_name, url_args=None, method='get', **headers):
        url = reverse(url_name, kwargs=url_args or {})

        if not hasattr(self.client, method):
            raise Exception('Metodo non valido ' + method)

        fn = getattr(self.client, method)
        return fn(url, **headers)

    def test_view_should_accept_only_post_requests(self):

        Access.objects.create(char=self.char, script=self.script)

        for method in ['get', 'put', 'patch', 'delete', 'head', 'options']:
            response = self._action('scripts:view', {'slug': self.script.hash}, method, **self.valid_headers)
            self.assertEqual(405, response.status_code)

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
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

    def test_view_should_check_for_access(self):
        """ Dobbiamo verificare che effettivamente l'utente abbia accesso allo script richiesto
        """

        Access.objects.create(char=self.char, script=self.script)

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(200, response.status_code)

    def test_view_access_with_expired_date(self):

        Access.objects.create(char=self.char, script=self.script, expire=now() - datetime.timedelta(days=1))

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(403, response.status_code)

    def test_view_access_with_future_expire(self):

        Access.objects.create(char=self.char, script=self.script, expire=now() + datetime.timedelta(days=1))

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(200, response.status_code)

    def test_view_should_fail_if_char_id_missing(self):
        Access.objects.create(char=self.char, script=self.script)
        self.valid_headers.pop('HTTP_X_CHARID')

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(403, response.status_code)
        self.assertTrue(Ban.objects.filter(ip=self.valid_headers['HTTP_X_FORWARDED_FOR']).exists())

    def test_view_should_fail_if_invalid_public_key(self):
        Access.objects.create(char=self.char, script=self.script)

        self.valid_headers['HTTP_X_KEY'] = '1' * 50

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)

        self.assertEquals(404, response.status_code)

    def test_view_should_check_if_invalid_char_id(self):
        Access.objects.create(char=self.char, script=self.script)

        self.valid_headers['HTTP_X_CHARID'] = 'XXXX'

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)

        self.assertEquals(403, response.status_code)

    def test_view_should_check_if_invalid_script_hash(self):
        Access.objects.create(char=self.char, script=self.script)
        self.valid_headers['HTTP_X_RANDOM_ID'] = 'invalid'

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(403, response.status_code)        

    def test_view_can_access_script(self):
        Access.objects.create(char=self.char, script=self.script)

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(200, response.status_code)

    def test_view_should_check_server_protocol(self):
        """ L'unico protocol accettato deve essere l'http 1.0
        """

        Access.objects.create(char=self.char, script=self.script)

        for value in ['HTTP/1.1', 'Random Strnig']:
            self.valid_headers['SERVER_PROTOCOL'] = value
            response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
            self.assertEquals(403, response.status_code)

    def test_view_should_update_character_name_and_shard(self):
        self.valid_headers['HTTP_X_SHARD'] = 'new_shard_name'
        self.valid_headers['HTTP_X_DECODE'] = 'new_char_name'

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)

        refresh = Char.objects.get(id=self.char.id)
        self.assertEquals('new_shard_name', refresh.shard)
        self.assertEquals('new_char_name', refresh.name)

    def test_view_should_fail_if_missing_shard_name(self):
        del self.valid_headers['HTTP_X_SHARD']

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(403, response.status_code)

    def test_view_should_fail_if_missing_char_name(self):
        del self.valid_headers['HTTP_X_DECODE']

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post', **self.valid_headers)
        self.assertEquals(403, response.status_code)

class UtilsTestCase(TestCase):

    def test_can_encrypt_message(self):
        key = "boom"
        message = "ihadadream"
        result = "aWhhZGFkcmVhbQ=="

        self.assertEquals(result, encrypt(message, key))

    def test_can_decrypt_message(self):
        key = "boom"
        message = "aWhhZGFkcmVhbQ=="
        result = "ihadadream"

        self.assertEquals(result, decrypt(message, key))