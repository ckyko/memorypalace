from django.shortcuts import render, render_to_response
from django.http import HttpResponse

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

def palace_library(req):
    return render_to_response('palace_library.html',data)
