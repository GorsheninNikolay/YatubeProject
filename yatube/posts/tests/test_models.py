from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Group

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username='Kolya')
        cls.post = Post.objects.create(
            text=5 * 'test',
            author=user,
        )

        cls.group = Group.objects.create(
            title='Test_Group',
            description='Test_description',
            slug='test-task'
        )

    def test_post_str_returned(self):
        """Str type returned for Post"""
        post = PostsModelTest.post
        expected_object_name = post.text
        self.assertEquals(expected_object_name, str(post))

    def test_GroupStr_returned(self):
        """Str type returned for Group"""
        group = PostsModelTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))
