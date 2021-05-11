from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from posts.models import Post, Group

from http import HTTPStatus

User = get_user_model()


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='AndreyG')
        cls.group = Group.objects.create(
            title='Test_Group',
            slug='test-slug')
        cls.post = Post.objects.create(
            text='Тестовый заголовок',
            author=cls.user,
            group=cls.group)

    def setUp(self):
        self.guest_client = Client()

    def test_urls_about_author(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_about_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
