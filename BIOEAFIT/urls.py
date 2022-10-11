"""BIOEAFIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from appBIOEAFIT.views import inicio, puntos, bonificaciones, asignarPuntos, redimir, puntos1, informacion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio),
    path('puntos/', puntos),
    path('puntos/asignarpuntos/', asignarPuntos),
    path('bonificaciones/<name>', bonificaciones),
    path('redimir/<name>/<int:puntosbono>', redimir),
    path('puntos1/', puntos1),
    path('informacion/', informacion), 
]