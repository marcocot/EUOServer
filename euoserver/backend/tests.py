from django.core.urlresolvers import reverse
from django.test import TestCase
from autofixture import AutoFixture
from .models import Script, Char


class ScriptViewTestCase(TestCase):
    def setUp(self):
        self.script = AutoFixture(Script).create_one()

    def _action(self, url_name, url_args=None, method='get'):
        url = reverse(url_name, kwargs=url_args or {})

        if not hasattr(self.client, method):
            raise Exception('Metodo non valido ' + method)

        fn = getattr(self.client, method)
        return fn(url)

    def test_view_should_accept_only_post_requests(self):
        for method in ['get', 'put', 'patch', 'delete', 'head', 'options']:
            response = self._action('scripts:view', {'slug': self.script.hash}, method)
            self.assertEqual(405, response.status_code)

        response = self._action('scripts:view', {'slug': self.script.hash}, 'post')
        self.assertEqual(200, response.status_code)


class ScriptModelTestCase(TestCase):
    def test_compute_hash_on_save(self):
        script = Script()
        script.save()

        self.assertIsNotNone(script.hash, "Non e' stato generato l'hash per lo script")