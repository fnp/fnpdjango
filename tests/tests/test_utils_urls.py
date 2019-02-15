from django.test import TestCase


class UrlsTestCase(TestCase):
    def test_i18n_patterns(self):
        self.assertEqual(self.client.get('/').content.decode('latin1'), 'pl')
        self.assertEqual(self.client.get('/en/').content.decode('latin1'), 'en')
