from rest_framework import serializers
from coreapp.models import PalaceObject, PalaceRoom, UserPalace

class UserPalaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserPalace
        fields=('user', 'palaceName', 'numOfRooms', 'public')

class PalaceRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalaceRoom
        fields = ('UserPalace', 'roomName', 'backgroundImage')

class PalaceObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalaceObject
        fields = ('palaceRoom', 'description', 'objectImage', 'width', 'height', 'position_X', 'position_Y')



