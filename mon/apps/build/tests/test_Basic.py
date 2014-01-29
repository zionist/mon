from django.test import TestCase
from django.test.client import Client

class BasicLogin(TestCase):
    def setUp(self):
        self.c = Client()

    def test_can_login(self):
        # The description should be set in the configuration file
        responce = self.c.post("/login/", {
            'username': 'admin',
            'password': 'admin',
            'next': '/main/',
        })
        self.assertEqual(responce.status_code, 200)
