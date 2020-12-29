from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
from doitforme.forms import AddServerForm
# from utils import SSHClient
from doitforme.models import Servers


def index(request):
    return render(request, 'home.html')


@login_required
def index(request):
    servers = Servers.objects.all()
    context = {'servers': servers}
    return render(request, 'home.html', context)


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'home.html')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)


@login_required
def add_server(request):
    context = {}
    form = AddServerForm(request.POST or None)
    if request.method == 'POST':
        form = AddServerForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('home')
    context['form'] = form
    return render(request, 'server_operations/add.html', context)


@login_required
def server_details(request, server_id):
    context = {}
    server = Servers.objects.get(id=server_id)
    if server:
        context['server'] = server
    return render(request, 'server_operations/details.html', context)
