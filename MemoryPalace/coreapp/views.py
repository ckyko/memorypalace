from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from coreapp.models import Users
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username: ',max_length=50)
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email:')

# Create your views here.
data = { 'title': 'MemoryPalace', 'char1': 'images/char1.png' }

def index(req):
    return render_to_response('home.html',data)

def MemoryPalace(req):
    return render_to_response('memory_palace.html',data)

def about(req):
    return render_to_response('about.html',data)

def contact(req):
    return render_to_response('contact.html',data)

def login(req):
    return render_to_response('login.html',data)

def register(req):
    if req.method == "POST":
        userForm = RegisterForm(req.POST, req.FILES)
        if userForm.is_valid():
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            email = userForm.cleaned_data['email']
            user = Users()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            return render(req,'profile.html',user)
    else:
        userForm = RegisterForm()

    return render_to_response('register.html', {'userForm':userForm})