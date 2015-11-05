from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
def room(req):

    return render_to_response('room.html',{ 'title': 'room'})
	
	
def index(req):

    return render_to_response('index.html',{ 'title': 'homepage'})