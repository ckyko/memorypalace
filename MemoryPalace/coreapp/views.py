from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
def index(req):
    data = { 'title': 'MemoryPalace'}
    return render_to_response('home.html',data)

def MemoryPalace(req):
    data = { 'title': 'MemoryPalace'}
    return render_to_response('memory_palace.html',data)
