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
from appBIOEAFIT.views import adminBonos, administrador, editarBonos, eliminarBonos, eliminarStudent, inicio, inicio1, inicioUser, bonificaciones, redimir, puntos1, informacion, signin, registro, signout, editar, registroadministrador, informacion1
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('inicio1/<mensaje>/<int:puntos>', inicio1),
    path('bonificaciones/<name>', bonificaciones),
    path('redimir/<name>/<int:puntosbono>', redimir),
    path('puntos1/', puntos1),
    path('informacion/', informacion),
    path('informacion1/<name>', informacion1),
    path('signin/', signin),
    path('registro/', registro),
    path('administrador/', administrador),
    path('eliminarStudent/<name>', eliminarStudent),
    path('adminBonos/', adminBonos),
    path('eliminarBonos/<name>', eliminarBonos),
    path('signout/', signout),
    path('inicioUser/<name>', inicioUser),
    path('editar/', editar),
    path('editarBonos/', editarBonos),
    path('registroadministrador/', registroadministrador)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
