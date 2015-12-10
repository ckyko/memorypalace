from rest_framework import serializers
from coreapp.models import PalaceObject, PalaceRoom, UserPalace
from django.contrib.auth.models import User



"""
Serializer of the the Palace Objects

This is the only serializer needed considering we just need the
palace objects to dyanamically update.
"""
class PalaceObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalaceObject
        fields = ('user', 'userPalace', 'palaceRoom', 'description',
                  'objectImage','width', 'height', 'position_x', 'position_y')



