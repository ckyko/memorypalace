from django.db import models
from django.contrib.auth.models import User

"""
User Palace Table
Contains the Memory Palaces for the user.

user: The foriegn key to connect it to a user
palaceName: The name of the Memory Palace and is Unique for each user
so a user can't have 2 palaces with the same name
numOfRooms: The number of rooms in the palace
public: Whether the Palace is public or not false by default

"""
class UserPalace(models.Model):
    user = models.ForeignKey(User,null=True)
    palaceName = models.CharField(max_length=200, unique=True,null=True)
    # BackgroundImage = models.CharField(max_length=200)
    numOfRooms = models.IntegerField(default=0)
    public = models.BooleanField(default=False)
    def __unicode__(self):
        return self.palaceName
    class Meta:
        unique_together = (("user", "palaceName"),)

"""
Palace Room Table
Contains the rooms in the Palace

userPalace: The foriegn key to the Palace the room belongs in
roomName: The name of the room coupled with the Palace so that they are named
uniqely for their palace
backgroundImage: The background Image of the room
"""
class PalaceRoom(models.Model):
    userPalace = models.ForeignKey('UserPalace',null=True)
    #palaceName = models.ForeignKey(UserPalace.palaceName,null=True)
    roomName = models.CharField(max_length=200, unique=True)
    backgroundImage = models.ImageField(upload_to='./coreapp/static/images', default='./coreapp/static/images/room.jpg')
    def __unicode__(self):
        return self.roomName
    class Meta:
        unique_together = (("userPalace", "roomName"),)

"""
Palace Object Table
Contains the objects inside a room

palaceRoom: The foriegn key that gives you the room the object belongs in.
objectName: The name of the object unique to the room it is inside
objectImage: The image used for the object
"""
class PalaceObject(models.Model):
    palaceRoom = models.ForeignKey('PalaceRoom',null=True)
    #palaceName = models.ForeignKey(UserPalace.palaceName,null=True)
    #roomName = models.ForeignKey(PalaceRoom.roomName,null=True)
    objectName= models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    # ObjectImage = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./coreapp/static/images', default='./coreapp/static/images/char2.png')
    def __unicode__(self):
        return self.objectName
    class Meta:
        unique_together = (("palaceRoom", "objectName"),)