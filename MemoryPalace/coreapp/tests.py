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

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_memory_palace_page(self):
        response = self.client.get(reverse('MemoryPalace'))
        self.assertEqual(response.status_code, 200)

    def test_palace_library_page(self):
        response = self.client.get(reverse('palace_library'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_createPalace(self):
        response = self.client.get(reverse('createPalace'))
        self.assertEqual(response.status_code, 302)

    def test_createRoom(self):
        response = self.client.get(reverse('createRoom'))
        self.assertEqual(response.status_code, 302)

    def test_register_with_new_user(self):
        response = self.client.post(reverse('register'), {'username': 'newUserName',
                                                           'password1': 'password',
                                                           'password2': 'password'})
        new_user = User.objects.get(username='newUserName')
        self.assertTrue(new_user is not None, msg="user not create.")

    def test_login_with_a_user(self):
        user = User.objects.create_user(username="testing", password="password")
        self.assertTrue(user is not None, msg="user not create.")
        response = self.client.post(reverse('login'), {'username': 'testing',
                                                         'password': 'password'})




class UserPalaceDataBaseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testing", password="password")
        user_palace = UserPalace.objects.create(user=user, palaceName='testing palace')
        palace_room = PalaceRoom.objects.create(userPalace=user_palace, roomName="testing room")
        PalaceObject.objects.create(palaceRoom=palace_room, description="testing palace object")

    def test_palace_room_object_create_in_database_or_not(self):
        user = User.objects.get(username="testing")
        self.assertTrue(user is not None, msg="user not create.")
        user_palace = UserPalace.objects.get(user=user)
        self.assertTrue(user_palace is not None, msg="user_palace not create.")
        user_room = PalaceRoom.objects.get(userPalace=user_palace)
        self.assertTrue(user_room is not None, msg="user_room not create.")
        palace_object = PalaceObject.objects.get(palaceRoom=user_room)
        self.assertTrue(palace_object is not None, msg="palace_object not create.")



    def tearDown(self):
        del self


# class RegisterTestCase(TestCase):
#     @patch.object(views, 'request')
#     def test_register_username_with_testing(self):
