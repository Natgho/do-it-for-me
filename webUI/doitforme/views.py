from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.
from doitforme.forms import AddServerForm
from doitforme.models import Servers
from sub_utils.utilities import SSHClient


def index(request):
    return render(request, 'home.html')


@login_required
def index(request):
    # messages.add_message(request, messages.INFO, 'Hello world.')
    # messages.add_message(request, messages.WARNING, 'Hello world2.')
    # messages.add_message(request, messages.ERROR, 'Hello world2.')
    servers = Servers.objects.filter(owner=request.user)
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
    server = Servers.objects.get(id=server_id, owner=request.user)
    if server:
        context['server'] = server
    return render(request, 'server_operations/details.html', context)


@login_required
def connection_check(request, server_id):
    server = Servers.objects.get(id=server_id, owner=request.user)
    try:
        ssh_client = SSHClient(ip=server.ip_address,
                               username=server.username,
                               password=server.password,
                               current_location='management')
        status = True
    except Exception as e:
        print(e)
        status = False
    return JsonResponse({'status': status})
