from django.db import models
from django.contrib.auth.models import User



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

class PalaceRoom(models.Model):
    userPalace = models.ForeignKey('UserPalace',null=True)
    #palaceName = models.ForeignKey(UserPalace.palaceName,null=True)
    roomName = models.CharField(max_length=200, unique=True)
    backgroundImage = models.ImageField(upload_to='./staticfiles/images', default='./staticfiles/images/room.jpg')
    def __unicode__(self):
        return self.roomName
    class Meta:
        unique_together = (("userPalace", "roomName"),)


class PalaceObject(models.Model):
    palaceRoom = models.ForeignKey('PalaceRoom',null=True)
    #palaceName = models.ForeignKey(UserPalace.palaceName,null=True)
    #roomName = models.ForeignKey(PalaceRoom.roomName,null=True)
    objectName= models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    # ObjectImage = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./staticfiles/images', default='./staticfiles/images/char2.png')
    def __unicode__(self):
        return self.objectName
    class Meta:
        unique_together = (("palaceRoom", "objectName"),)