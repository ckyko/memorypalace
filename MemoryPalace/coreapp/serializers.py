from rest_framework import serializers
from coreapp.models import PalaceObject, PalaceRoom, UserPalace
from django.contrib.auth.models import User



"""
Serializer of the the Palace Objects
"""
class PalaceObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalaceObject
        fields = ('user', 'userPalace', 'palaceRoom', 'description',
                  'objectImage','width', 'height', 'position_x', 'position_y')
