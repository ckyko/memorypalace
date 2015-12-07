from rest_framework import serializers
from coreapp.models import PalaceObject, PalaceRoom, UserPalace

class UserPalaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserPalace
        fields=('user', 'palaceName', 'numOfRooms', 'public')

class PalaceRoomSerializer(serializers.ModelSerializer):
    user = UserPalaceSerializer()

    class Meta:
        model = PalaceRoom
        fields = ('user', 'userPalace', 'roomName', 'backgroundImage')

class PalaceObjectSerializer(serializers.ModelSerializer):
    user = UserPalaceSerializer()
    palaceRoom = PalaceRoomSerializer()
    class Meta:
        model = PalaceObject
        fields = ('user', 'userPalace', 'palaceRoom', 'description', 'objectImage', 'width', 'height', 'position_X', 'position_Y')



