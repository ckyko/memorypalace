from django.db import models
from django.contrib.auth.models import User



class UserPalaces(models.Model):
    palaceName = models.CharField(max_length=200)
    # BackgroundImage = models.CharField(max_length=200)
    backgroundImage = models.ImageField(upload_to='./staticfiles/images', default='./staticfiles/images/room.jpg')
    user = models.ForeignKey(User,null=True)


class PalaceObjects(models.Model):

    objectName= models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # ObjectImage = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./staticfiles/images', default='./staticfiles/images/char2.png')
    userPalaces = models.ForeignKey('UserPalaces',null=True)


    def __unicode__(self):
        return self.ObjectName