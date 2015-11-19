from django.db import models
from django.contrib.auth.models import User



class UserPalaces(models.Model):
    palaceName = models.CharField(max_length=200)
    # BackgroundImage = models.CharField(max_length=200)
    backgroundImage = models.ImageField(upload_to='./upload/')
    user = models.ForeignKey(User)


class PalaceObjects(models.Model):

    objectName= models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # ObjectImage = models.CharField(max_length=200)
    objectImage = models.ImageField(upload_to='./upload/')


    userPalaces = models.ForeignKey(UserPalaces)


    def __unicode__(self):
        return self.ObjectName