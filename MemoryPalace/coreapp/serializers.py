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

        def create(self, validated_data):
            return PalaceObject.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.position_X = validated_data.get('position_X', instance.position_X)
            instance.position_Y = validated_data.get('position_Y', instance.position_Y)
            instance.width = validated_data.get('width', instance.width)
            instance.height = validated_data.get('height', instance.height)
            instance.save()
            return instance



