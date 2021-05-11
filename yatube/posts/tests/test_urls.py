from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='AndreyG')
        cls.user2 = User.objects.create_user(username='NotAndrey')
        cls.group = Group.objects.create(
            title='Test_Group',
            slug='test-slug')
        cls.post = Post.objects.create(
            text='Тестовый заголовок',
            author=cls.user,
            group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client2 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2.force_login(self.user2)

    def test_urls_main_page(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_group_page(self):
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_guest_client(self):
        response = self.guest_client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_urls_username(self):
        response = self.guest_client.get(f'/{self.user}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_username_post(self):
        response = self.guest_client.get(f'/{self.user}/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_username_post_edit_for_anonym(self):
        response = self.guest_client.get(f'/{self.user}/{self.post.id}/edit/')
        url = f'/auth/login/?next=/{self.user}/{self.post.id}/edit/'
        self.assertRedirects(response, url)

    def test_urls_username_post_edit_for_author(self):
        url = f'/{self.user}/{self.post.id}/edit/'
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_username_post_edit_for_notauthor(self):
        url = f'/{self.user}/{self.post.id}/edit/'
        response = self.authorized_client2.get(url)
        self.assertRedirects(response, f'/{self.user}/{self.post.id}/')

    def test_urls_about_author(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_about_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL uses correct template."""
        templates_url_names = {
            'base/index.html': '/',
            'posts/new_post.html': '/new/',
            'group.html': f'/group/{self.group.slug}/',
            'posts/post_edit.html': f'/{self.user}/{self.post.id}/edit/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
