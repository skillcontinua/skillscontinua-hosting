# File path: C:\hosting\skillscontinua_hosting\village\tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import ForumTopic


class VillageSmokeTests(TestCase):
    """Minimal smoke tests — these turn green once views/urls are wired."""

    def test_village_home_renders(self):
        response = self.client.get(reverse("village:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "village/home.html")

    def test_post_list_renders(self):
        response = self.client.get(reverse("village:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "village/post_list.html")

    def test_media_list_renders(self):
        response = self.client.get(reverse("village:media_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "village/media_list.html")

    def test_forum_list_renders(self):
        response = self.client.get(reverse("village:forum_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "village/forum_list.html")

    def test_anonymous_cannot_post_reply(self):
        User = get_user_model()
        author = User.objects.create_user(username="starter", password="pw12345!")
        topic = ForumTopic.objects.create(
            title="Test topic",
            slug="test-topic",
            started_by=author,
            pillar_tag="General",
            body="Body text",
        )
        response = self.client.post(
            f"/village/forum/{topic.slug}/",
            {"message": "Anonymous attempt"},
        )
        # Anonymous POST should redirect to login, and no reply created.
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
        self.assertEqual(topic.replies.count(), 0)

    def test_logged_in_user_can_post_reply(self):
        User = get_user_model()
        author = User.objects.create_user(username="starter2", password="pw12345!")
        replier = User.objects.create_user(username="replier", password="pw12345!")
        topic = ForumTopic.objects.create(
            title="Another topic",
            slug="another-topic",
            started_by=author,
            pillar_tag="General",
            body="Body text",
        )
        self.client.force_login(replier)
        response = self.client.post(
            f"/village/forum/{topic.slug}/",
            {"message": "This is a helpful reply."},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(topic.replies.count(), 1)
        reply = topic.replies.first()
        self.assertEqual(reply.author, replier)
        self.assertFalse(reply.is_verified_mentor_answer)  # not a mentor