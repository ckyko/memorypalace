from django.db import models

# Create your models here.
class Users(models.Model):
	Username = models.CharField(max_length=20)
	Email = models.CharField(max_length=200)
	#EncryptedPassword

class UserPalaces(models.Model):
	#Username = models.ForeignKey(Users)
	PalaceName = models.CharField(max_length=200)
	BackgroundImage = models.ImageField()

class PalaceObjects(models.Model):
    #Username = models.ForeignKey(Users)
    # #PalaceName = models.ForeignKey(UserPalaces)
    ObjectName= models.CharField(max_length=200)
    #FileLocation(Coordinates on page)
    Description = models.CharField(max_length=200)
    ObjectImage = models.ImageField()