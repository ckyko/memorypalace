from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from coreapp.views import index


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>MemoryPalace</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
