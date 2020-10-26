from django.shortcuts import render

# Create your views here.
from utils import SSHClient


def index(request):
    return render(request, 'home.html')
