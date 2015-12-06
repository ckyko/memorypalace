from django import forms
from django.forms import ModelForm
from .models import PalaceRoom, UserPalace
# from django.contrib.auth.models import User

# class CreatePalaceForm(forms.Form):
#     palaceName = forms.CharField()
#     numOfRooms = forms.IntegerField()
#     public = forms.BooleanField(initial=False)

class CreatePalaceForm(ModelForm):
    class Meta:
        model = UserPalace
        fields = ['palaceName', 'numOfRooms', 'public']

# class CreateRoomForm(forms.Form):
#     roomName = forms.CharField()
#     backgroundImage = forms.ImageField()
class CreateRoomForm(ModelForm):
    class Meta:
        model = PalaceRoom
        fields = [ 'roomName', 'backgroundImage']