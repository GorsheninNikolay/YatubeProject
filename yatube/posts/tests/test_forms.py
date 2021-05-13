import shutil
import tempfile
from http import HTTPStatus

from django.urls import reverse
from django.conf import settings
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, Comment

User = get_user_model()


class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = User.objects.create_user(username='AndreyG1')
        cls.group = Group.objects.create(
            title='Test_Group',
            slug='test-slug'
        )
        cls.another_group = Group.objects.create(
            title='Another_Group',
            slug='another-group'
        )
        cls.post = Post.objects.create(
            text='Test',
            author=cls.user,
            group=cls.group
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_form(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Random',
            'group': self.group.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/')
        self.assertTrue(
            Post.objects.filter(
                text='Random',
                group=self.group.id,
                image='posts/small.gif').exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_client_comment(self):
        form_data = {
            'text': 'Comment!',
            'author': self.user.id
        }
        response = self.authorized_client.post(
            reverse('add_comment', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'post', args=[self.user, self.post.id]))
        self.assertTrue(Comment.objects.all().count() == 1)
        url = f'/{self.user}/{self.post.id}/comment/'
        response = self.guest_client.get(url)
        self.assertRedirects(response, '/auth/login/?next=' + url)

    def test_guest_cant_comment(self):
        form_data = {
            'text': 'Comment!',
            'author': self.user.id
        }
        response = self.guest_client.post(
            reverse('add_comment', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )
        url = f'/{self.user}/{self.post.id}/comment/'
        response = self.guest_client.get(url)
        self.assertRedirects(response, '/auth/login/?next=' + url)
        self.assertTrue(Comment.objects.all().count() == 0)

    def test_post_edited_form(self):
        posts_count = Post.objects.count()
        url = reverse('post_edit', args=[self.user, self.post.id])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form_data = {
            'text': 'Test2',
            'group': self.another_group.id,
        }
        response = self.authorized_client.post(
            reverse('post_edit', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(pk=self.post.id)
        self.assertRedirects(response, f'/{self.user}/{self.post.id}/')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)
