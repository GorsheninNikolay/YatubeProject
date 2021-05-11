from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.cache.utils import make_template_fragment_key

from posts.models import Post, Group

User = get_user_model()


class CacheTests(TestCase):
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

    def test_cache(self):
        cache = make_template_fragment_key('index_page')
        self.assertTrue(cache)
