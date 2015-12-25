"""
test_models
Tests the database models of the project
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from coreapp.models import UserPalace, PalaceRoom, PalaceObject


class UserPalaceDataBaseTestCase(TestCase):
    """
    Tests wheather the dastabase adds the models as its supposed to
    """
    def setUp(self):
        """
        Inputs tests data for the test
        :return:
        """
        user = User.objects.create_user(username="testing",
                                        password="password")
        user_palace = UserPalace.objects.create(user=user,
                                                palaceName='testing palace')
        palace_room = PalaceRoom.objects.create(userPalace=user_palace,
                                                roomName="testing room")
        PalaceObject.objects.create(palaceRoom=palace_room,
                                    description="testing palace object")

    def test_palace_room_object_create_in_database_or_not(self):
        """
        Testing object creation
        :return:
        """
        user = User.objects.get(username="testing")
        self.assertTrue(user is not None, msg="user not create.")
        user_palace = UserPalace.objects.get(user=user)
        self.assertTrue(user_palace is not None, msg="user_palace not create.")
        user_room = PalaceRoom.objects.get(userPalace=user_palace)
        self.assertTrue(user_room is not None, msg="user_room not create.")
        palace_object = PalaceObject.objects.get(palaceRoom=user_room)
        self.assertTrue(palace_object is not None,
                        msg="palace_object not create.")

    def test_palaceName(self):
        """
        Test creating a memory palace
        :return:
        """
        user_palace = UserPalace.objects.get(palaceName='testing palace')
        self.assertTrue(user_palace is not None,
                        msg="palace name is create not correct")
        self.assertEqual(user_palace.__unicode__(), user_palace.palaceName)

    def test_roomName(self):
        """
        Test if the Room naem i
        :return:
        """
        palace_room = PalaceRoom.objects.get(roomName="testing room")
        self.assertTrue(palace_room is not None,
                        msg="room name is create not correct")
        self.assertEqual(palace_room.__unicode__(), palace_room.roomName)

    def tearDown(self):
        """
        deletes new data from test
        :return:
        """
        del self
