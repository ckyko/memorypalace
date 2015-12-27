"""
Serializer
Puts the objects in serial to save them
"""
from rest_framework import serializers
from coreapp.models import PalaceObject, PalaceRoom, UserPalace
from django.contrib.auth.models import User


class PalaceObjectSerializer(serializers.ModelSerializer):
    """
    This is the only serializer needed considering we just need the
    palace objects to dyanamically update.
    """
    class Meta:
        """
        Select a model
        """
        model = PalaceObject
        fields = ('user', 'userPalace', 'palaceRoom', 'description',
                  'objectImage', 'width', 'height', 'position_x', 'position_y')

        def create(self, validated_data):
            """
            Make a new PalaceObject for the database
            """
            return PalaceObject.objects.create(**validated_data)

        def update(self, instance, validated_data):
            """
            Update PalaceObject
            """
            instance.position_X = validated_data.get('position_X', instance.position_X)
            instance.position_Y = validated_data.get('position_Y', instance.position_Y)
            instance.width = validated_data.get('width', instance.width)
            instance.height = validated_data.get('height', instance.height)
            instance.save()
            return instance
