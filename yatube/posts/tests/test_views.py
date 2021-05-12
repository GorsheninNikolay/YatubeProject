import shutil
import tempfile
from typing import Optional

from django import forms, http
from django.conf import settings
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, Follow

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username='AndreyG1')
        cls.another_user = User.objects.create_user(username='NotAndrey')
        cls.group = Group.objects.create(
            title='Test_Group',
            slug='test-slug'
        )
        cls.fake_group = Group.objects.create(
            title='Fake_Group',
            slug='fake'
        )
        cls.post = Post.objects.create(
            text='Test',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.another_authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(self.user)
        self.another_authorized_client.force_login(self.another_user)

    def post_fields_test(self, response: http,
                         page: str, n: Optional[int] = None) -> None:
        if n is not None:
            page_object = response.context[page][n]
        else:
            page_object = response.context[page]
        post_id = page_object.id
        text = page_object.text
        author = page_object.author
        date = page_object.pub_date
        self.assertEqual(post_id, self.post.id)
        self.assertEqual(text, self.post.text)
        self.assertEqual(author, self.user)
        self.assertEqual(date, self.post.pub_date)
        self.assertContains(response, '<img')

    def test_pages_use_correct_template(self):
        """URL uses correct template."""
        templates_pages_names = {
            'base/index.html': reverse('index'),
            'posts/new_post.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': self.group.slug})
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_shows_correct_context(self):
        """Template new_post gets the correct form fields."""
        responses = {
            'new_post': reverse('new_post'),
            'post_edit': reverse('post_edit', args=[self.user, self.post.id]),
        }
        form_fields = {
            'group': forms.models.ModelChoiceField,
            'text': forms.fields.CharField,
        }
        for view, reverse_name in responses.items():
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    response = self.authorized_client.get(reverse_name)
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_group_shows_correct_context(self):
        """Group formed with correct context."""
        reverse_name = reverse('group_posts', args=[self.group.slug])
        response = self.guest_client.get(reverse_name)
        group_object = response.context['group']
        group_description = group_object.description
        group_title = group_object.title
        self.post_fields_test(response, 'page', 0)
        self.assertEqual(group_description, self.group.description)
        self.assertEqual(group_title, self.group.title)

    def test_post_shows_correct_context(self):
        """Post formed with correct context."""
        response = self.guest_client.get(reverse('post',
                                         args=[self.user, self.post.id]))
        self.post_fields_test(response, 'post')

    def test_profile_shows_correct_context(self):
        """Profile formed with correct context."""
        response = self.guest_client.get(reverse('profile',
                                         args=[self.user]))
        self.post_fields_test(response, 'page', 0)
        self.assertEqual(response.context['author'].username,
                         self.user.username)

    def test_post_doesnt_show_on_the_another_group(self):
        """Post doesnt show on the another group."""
        reverse_name = reverse('group_posts', args=[self.fake_group.slug])
        response = self.guest_client.get(reverse_name)
        self.assertTrue(len(response.context['page']) == 0)

    def test_index_shows_correct_context(self):
        """Index gets the correct context."""
        response = self.guest_client.get(reverse('index'))
        self.post_fields_test(response, 'page', 0)

    def test_posts_following_authors(self):
        """Follow_index gets the correct context"""
        reverse_follow = reverse('profile_follow', args=[self.user])
        self.another_authorized_client.get(reverse_follow)
        response = self.another_authorized_client.get(
            reverse('follow_index'))
        self.post_fields_test(response, 'page', 0)

    def test_posts_follower_authors(self):
        """Post locate on the author page"""
        reverse_follow = reverse('profile_follow', args=[self.user])
        self.another_authorized_client.get(reverse_follow)
        self.assertEqual(Follow.objects.all().count(), 1)

    def test_posts_follower_authors_dont_shows(self):
        """Post dont locate on the page another author"""
        response = self.authorized_client.get(reverse('follow_index'))
        self.assertTrue(len(response.context['page']) == 0)

    def test_follow(self):
        """User can follow for the another user"""
        reverse_follow = reverse('profile_follow', args=[self.user])
        response = self.another_authorized_client.get(reverse_follow)
        self.assertTrue(Follow.objects.all().count() == 1)
        self.assertRedirects(response, reverse('profile', args=[self.user]))

    def test_unfollow(self):
        """Usern can unfollow from the another user"""
        self.another_authorized_client.get(reverse('profile_follow',
                                                   args=[self.user]))
        self.assertTrue(Follow.objects.all().count() == 1)
        response = self.another_authorized_client.get(reverse(
            'profile_unfollow',
            args=[self.user]))
        self.assertTrue(Follow.objects.all().count() == 0)
        self.assertRedirects(response, reverse('profile', args=[self.user]))


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='AndreyG1')
        cls.group = Group.objects.create(
            title='Test_Group',
            slug='test-slug'
        )
        cls.fake_group = Group.objects.create(
            title='Fake_Group',
            slug='fake'
        )
        Post.objects.bulk_create([
            Post(text='This is a test',
                 group=cls.group, author=cls.user) for num in range(13)
        ])

    def setUp(self):
        self.guest_client = Client()

    def test_page_contains_ten_records(self):
        # Проверка: на первой странице должно быть 10 постов.
        reverses = {
            'index': reverse('index'),
            'profile': reverse('profile', args=[self.user]),
            'group_posts': reverse('group_posts', args=[self.group.slug])
        }
        for name, reverse_name in reverses.items():
            with self.subTest(name=name):
                response = self.guest_client.get(reverse_name)
                _object = len(response.context.get('page').object_list)
                self.assertEqual(_object, 10)

    def test_page_contains_three_records(self):
        # Проверка: на второй странице должно быть 3 поста.
        reverses = {
            'index': reverse('index'),
            'profile': reverse('profile', args=[self.user]),
            'group_posts': reverse('group_posts', args=[self.group.slug])
        }
        for name, reverse_name in reverses.items():
            with self.subTest(name=name):
                response = self.guest_client.get(reverse_name + '?page=2')
                _object = len(response.context.get('page').object_list)
                self.assertEqual(_object, 3)
