from django.test import TestCase


class MiddlewareTests(TestCase):
    def test_realip(self):
        self.assertEqual(
            self.client.get('/ip/').content.decode('latin1'),
            '127.0.0.1'
        )
        self.assertEqual(
            self.client.get(
                '/ip/',
                HTTP_X_REAL_IP='1.2.3.4'
            ).content.decode('latin1'),
            '1.2.3.4'
        )
