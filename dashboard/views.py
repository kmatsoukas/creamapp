from django.shortcuts import render
from django.http import HttpResponse
import socket


# show the ip of the server
def show_ip(request):
    return HttpResponse(socket.gethostbyname(socket.gethostname()))
