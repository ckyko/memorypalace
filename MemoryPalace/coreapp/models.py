"""
Models.py

This is where all the models of the database are contained
"""
from django.db import models
from django.contrib.auth.models import User

"""
User Palace Table
Contains the Memory Palaces for the user.
"""
class UserPalace(models.Model):
    """
    user: The foreign key to connect it to a user
    palaceName: The name of the Memory Palace and is Unique for each user
    so a user can't have 2 palaces with the same name
    numOfRooms: The number of rooms in the palace
    public: Whether the Palace is public or not false by default
    """
    user = models.ForeignKey(User, null=True)
    palaceName = models.CharField(max_length=200, unique=True, null=True)
    numOfRooms = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.palaceName

    class Meta:
        unique_together = (("user", "palaceName"),)

"""
Palace Room Table
Contains the rooms in the Palace
"""
class PalaceRoom(models.Model):
    """
    userPalace: The foriegn key to the Palace the room belongs in
    roomName: The name of the room coupled with the Palace so that they are
    named uniqely for their palace
    backgroundImage: The background Image of the room
    """
    user = models.ForeignKey(User, null=True)
    userPalace = models.ForeignKey('UserPalace', null=True)
    roomName = models.CharField(max_length=200, unique=True)
    backgroundImage = models.ImageField(upload_to='./static/images', default='./static/images/room.jpg')

    def __unicode__(self):
        return self.roomName

    class Meta:
        unique_together = (("userPalace", "roomName"),)

"""
Palace Object Table
Contains the objects inside a room
"""
class PalaceObject(models.Model):
    """
    palaceRoom: The foriegn key that gives you the room the object belongs in.
    objectName: The name of the object unique to the room it is inside
    objectImage: The image used for the object
    x: The x coordinate of the object in the room
    y: The y coordinate of the object in the room
    """
    user = models.ForeignKey(User, null=True)
    userPalace = models.ForeignKey('UserPalace', null=True)
    palaceRoom = models.ForeignKey('PalaceRoom', null=True)
    # objectName= models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./coreapp/static/images'),
    # ObjectImage = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./static/images/memory_objects', default='./static/images/char2.png')
    width = models.IntegerField(default=50)
    height = models.IntegerField(default=50)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)

    def __unicode__(self):
        return self.description

    class Meta:
        unique_together = (("palaceRoom", "description"),)
