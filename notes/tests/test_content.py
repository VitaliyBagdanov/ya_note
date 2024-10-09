from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=cls.author,
        )
        cls.detail_url = reverse('notes:list')

    def test_notes_list_for_different_users(self):
        users = (
            (self.author, True),
            (self.reader, False),
        )
        for user, status in users:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(self.detail_url)
                object_list = response.context['object_list']
                if status:
                    self.assertIn(self.note, object_list)
                else:
                    self.assertNotIn(self.note, object_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(self.detail_url)
        self.client.force_login(self.author)
        response = self.auth_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
