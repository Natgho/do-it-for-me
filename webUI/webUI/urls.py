"""webUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from doitforme import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='home'),
    path('accounts/sign_up/', views.sign_up, name="sign-up"),
    path('server/add', views.add_server, name="add_server"),
    path('server/<int:server_id>', views.server_details, name="server_details"),
    path('server/status/<int:server_id>', views.connection_check, name="connection_check"),
    path('server/log/<int:server_id>', views.get_logs, name="get_logs"),
    path('server/log/remove/<int:server_id>', views.clear_logs, name="clear_logs"),
    path('server/docker/install/<int:server_id>', views.install_docker, name="install_docker")
]
