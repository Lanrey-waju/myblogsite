from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.urls import reverse
from .models import Post
from django.utils import timezone

User = get_user_model()


# Create your tests here.
class BlogPostTests(TestCase):

    def setUp(self):
        url = reverse("blog:home")
        self.response = self.client.get(url)
        self.post = Post.objects.create(
            title="Dummy Post",
            slug="dummy-post",
            author=User.objects.create(email="user@example.com", password="foo"),
            body="Body of dummy post",
            # publish = timezone.now()
        )

    def test_post_creation(self):
        self.assertEqual(f"{self.post.title}", "Dummy Post")
        self.assertEqual(f"{self.post.slug}", "dummy-post")
        self.assertEqual(f"{self.post.author}", "user@example.com")
        self.assertEqual(f"{self.post.body}", "Body of dummy post")
        # self.assertEqual(f'{self.post.publish}', timezone.now)

    def test_post_list_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, "Posts")
        self.assertTemplateUsed(self.response, "blog/post_list.html")
        self.assertTemplateNotUsed(self.response, "blog/post_detail.html")


class BlogViewTests(TestCase):
    """Test module for the views logic of the blog"""

    def setUp(self):
        pass
