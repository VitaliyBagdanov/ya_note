from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        # cls.note = Note.objects.create(
        #     title='Заголовок',
        #     text='Текст',
        #     slug='note-slug',
        #     author=cls.author,
        # )
        # Создаём двух пользователей с разными именами:
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

    def test_page_availability_for_anonymous_user(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = ('notes:list', 'notes:add', 'notes:success')
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.auth_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
