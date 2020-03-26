from django.test import TestCase
from django.contrib.auth.models import User
from ..models import SomeModel


class ActionsTests(TestCase):
    def test_csv(self):
        u = User(username='user', is_superuser=True, is_staff=True)
        u.set_password('test')
        u.save()

        SomeModel.objects.create()

        self.client.login(username='user', password='test')

        response = self.client.post(
            '/admin/tests/somemodel/',
            {
                'action': 'export_as_csv',
                '_selected_action': '1',
            }
        )
        self.assertEqual(
            response.content,
            b"id,attachment\r\n1,\r\n")
        
