from django.db import models

class Users(models.Model):
    Username = models.CharField(max_length=20,primary_key=True)
    Email = models.CharField(max_length=200)
    #EncryptedPassword

class UserPalaces(models.Model):
    #Username = models.ForeignKey(Users)
    PalaceName = models.CharField(max_length=200)
    BackgroundImage = models.CharField(max_length=200)

class PalaceObject(models.Model):
    #Username = models.ForeignKey(Users)
    #  #PalaceName = models.ForeignKey(UserPalaces)
    ObjectName= models.CharField(max_length=200)
    #FileLocation(Coordinates on page)
    Description = models.CharField(max_length=200)
    ObjectImage = models.CharField(max_length=200)
    def __unicode__(self):
        return self.ObjectName