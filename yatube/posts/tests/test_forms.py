from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment

User = get_user_model()


class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            group=cls.group,
            image='posts/test.jpeg'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_form(self):
        posts_count = Post.objects.count()
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form_data = {
            'text': 'Random',
            'group': self.group.id,
            'image': self.post.image
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(text='Random')
        self.assertRedirects(response, '/')
        self.assertTrue(post.image)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertNotEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_comment_only_for_authorized_client(self):
        response = self.authorized_client.get(reverse(
            'post', args=[self.user, self.post.id]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form_data = {
            'text': 'Wow!',
            'author': self.user.id
        }
        response = self.authorized_client.post(
            reverse('post', args=[self.user, self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'post', args=[self.user, self.post.id]))
        self.assertTrue(Comment.objects.all().count() == 1)
        url = f'/{self.user}/{self.post.id}/comment/'
        response = self.guest_client.get(url)
        self.assertRedirects(response, '/auth/login/?next=' + url)

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
