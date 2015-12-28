"""
test_views.py
Tests if the all the views are functioning
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from coreapp import views


class ViewsTestCase(TestCase):
    """
    Class: ViewsTestCasepyli

    Tests the functions inside a room
    """
    def test_index_page(self):
        """
        Tests that the index page is running
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        """
        Tests that the about page is running
        """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        """
        Tests that the about contact is running
        """
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)


    def test_memory_palace_page(self):
        """
        Tests memory Palace page is running
        """
        response = self.client.get(reverse('MemoryPalace'))
        self.assertEqual(response.status_code, 200)

    def test_palace_library_page(self):
        """
        Tests that the about palace_library page is running
        """
        response = self.client.get(reverse('palace_library'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Tests that the about register page is running
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        """
        Tests that the about login page is running
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_createPalace(self):
        """
        Tests the pages and transitions to createPalace page
        """
        response = self.client.get(reverse('createPalace'))
        self.assertEqual(response.status_code, 302)

    def test_createRoom(self):
        """
        Tests the pages and transitions to createPage page
        """
        response = self.client.get(reverse('createRoom'))
        self.assertEqual(response.status_code, 302)

    def test_register_with_new_user(self):
        """
        Test user Registration
        """

        response = self.client.post(reverse('register'),
                                           {'username': 'newUserName',
                                            'password1': 'password',
                                            'password2': 'password'})

        new_user = User.objects.get(username='newUserName')
        self.assertTrue(new_user is not None, msg="user not create.")

    def test_login_with_a_user(self):
        """
        Testing login
        """
        user = User.objects.create_user(username="testing", password="password")
        self.assertTrue(user is not None, msg="user not create.")
        response = self.client.post(reverse('login'), {'username': 'testing',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 302)
        index_response = self.client.get(reverse('index'))
        self.assertContains(index_response,
                            '<li><a class="modal-trigger" href=/logout>Logout</a></li>')



    def test_create_palace(self):
        """
        Tests creating a palace
        """
        user = User.objects.create_user(username="testing", password="password")
