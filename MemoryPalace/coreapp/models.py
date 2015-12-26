"""
    Models.py
    This is where all the models of the database are contained
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

class UserPalace(models.Model):
    """
        User Palace Table
        Contains the Memory Palaces for the user.
    """
    user = models.ForeignKey(User, null=True)
    palaceName = models.CharField(max_length=200, unique=True, null=True)
    # numOfRooms = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.palaceName

    class Meta:
        unique_together = (("user", "palaceName"),)


class PalaceRoom(models.Model):
    """
        Palace Room Table
        Contains the rooms in the Palace
    """
    user = models.ForeignKey(User, null=True)
    userPalace = models.ForeignKey('UserPalace', null=True)
    roomName = models.CharField(max_length=200, unique=True)
    backgroundImage = models.ImageField(upload_to='static/images/rooms')
    #,default='static/images/room.jpg'

    def __unicode__(self):
        return self.roomName

    class Meta:
        unique_together = (("user", "userPalace", "roomName"),)


class PalaceObject(models.Model):
    """
        Palace Object Table
        Contains the objects inside a palace
    """
    # user = models.ForeignKey(User, null=True)
    userPalace = models.ForeignKey('UserPalace', null=True)
    # palaceRoom = models.ForeignKey('PalaceRoom', null=True)
    description = models.CharField(max_length=200, default=" ")
    objectName = models.CharField(max_length=200, default="", unique=True)
    objectImage = models.ImageField(upload_to='./static/images/memory_objects')
    #,default='./static/images/char2.png')
    width = models.IntegerField(default=50)
    height = models.IntegerField(default=50)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    public = models.BooleanField(default=False)


    def __unicode__(self):
        return self.objectImage.url
    #
    class Meta:
        unique_together = (("userPalace", "objectName"),)


class RoomObject(models.Model):
    """
        Room Objects
        The objects in a room used from inside the palace
    """
    palaceRoom = models.ForeignKey('PalaceRoom', null=True)
    palaceObject = models.ForeignKey('PalaceObject', null=True)
    url = models.CharField(max_length=200, default=" ")
    note = models.CharField(max_length=200, default=" ")
    width = models.IntegerField(default=50)
    height = models.IntegerField(default=50)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)

    def __unicode__(self):
        return self.url

    class Meta:
        unique_together = (("palaceRoom", "url"),)


@receiver(post_delete, sender=PalaceRoom)
def PalaceRoom_post_delete_handler(sender, **kwargs):
    """
        Deletes objects available in the Palace
    """
    PalaceRoom = kwargs['instance']
    storage, path = PalaceRoom.backgroundImage.storage, PalaceRoom.backgroundImage.path
    storage.delete(path)

@receiver(post_delete, sender=PalaceObject)
def PalaceObject_post_delete_handler(sender, **kwargs):
    """
        Delete objects inside a room
    """
    PalaceObject = kwargs['instance']
    storage, path = PalaceObject.objectImage.storage, PalaceObject.objectImage.path
    storage.delete(path)

