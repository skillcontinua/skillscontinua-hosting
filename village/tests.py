# File path: C:\hosting\skillscontinua_hosting\village\tests.py
from django.test import TestCase
from django.urls import reverse


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