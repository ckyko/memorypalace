from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.http import HttpRequest
from .models import UserPalace, PalaceRoom, PalaceObject
from django.contrib.auth.models import User
from coreapp import views
from mock import patch

# URL_Dict = {'/': views.index, '/MemoryPalace/': views.MemoryPalace, '/about/': views.about, '/contact/': views.contact, '/login/': views.log_in, '/register/': views.register}
# #Dictionary to test multiple pages with same functionality
# class MemoryPalaceTest(TestCase):
#     #Test if the provided "value" is linked to the url
#     def test_root_url_resolves_to_URL_Dict_view(self):
#         for key,value in URL_Dict.items():
#             found = resolve(key)
#             self.assertEqual(found.func, value)
#     #Test if every HTML page contains basic tags
#     def test_URL_Dict_returns_correct_html(self):
#         request = HttpRequest()
#         for key,value in URL_Dict.items():
#             response = value(request)
#             self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
#             self.assertIn(b'<title>MemoryPalace</title>', response.content)
#             self.assertTrue(response.content.strip().endswith(b'</html>'))

    # def test_database(self):
    #     pObjNum= len(PalaceObject.objects.all())
    #     obj = PalaceObject("Char","This is a test feature","char2.png")
    #     obj.save()
    #     self.assertEqual(len(PalaceObject.objects.all()),pObjNum+1)


class ViewsTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

