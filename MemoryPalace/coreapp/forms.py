from django import forms
# from django.contrib.auth.models import User

class CreatePalaceForm(forms.Form):
    palaceName = forms.CharField()
    numOfRooms = forms.IntegerField()
    public = forms.BooleanField(required=False)

