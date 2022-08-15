from pipes import Template
from pydoc import doc
from xml.dom.minidom import Document
from django.shortcuts import render, redirect
from .models import Usuario, Puntos_Usuarios, Bonificacion

# Llamar inicio
def inicio(request):
    usuarios = Usuario.objects.all()
    nombreusuario = usuarios.values("nombre")
    nombreusuario = nombreusuario[0]
    return render(request, 'inicio.html', {"name": nombreusuario["nombre"]})

#Llamar intercambio con el usuario de prueba y su cantidad de puntos
def puntos(request):
    usuarios = Usuario.objects.all()
    nombreusuario = usuarios.values("nombre")
    nombreusuario = nombreusuario[0]
    puntos = Puntos_Usuarios.objects.all()
    cantidadp = puntos.values("cantidad")
    cantidadp= cantidadp[0]
    return render(request, 'puntos.html', {"name": nombreusuario["nombre"], "cantidad": cantidadp["cantidad"]})

#Metodo para convertir las botellas a puntos y asignarlos
def asignarPuntos(request):
    formulario = request.POST.dict()
    print(formulario)
    puntos = (int(request.POST['peso'])+int(request.POST['tamanio']))/(20+int(request.POST['calidad']))
    puntos = round(puntos)
    usuario=Usuario.objects.filter(nombre=request.POST['nombre'])
    listusuario = usuario.values()
    listusuario = listusuario[0]
    listusuario = listusuario['identificacion']
    print(listusuario)
    print("puntaje:" ,puntos)
    objeto_puntos = Puntos_Usuarios.objects.filter(identificacion_id=listusuario).values()
    list_objetos_puntos = objeto_puntos[0]
    cantidad_objetos_puntos = list_objetos_puntos['cantidad']
    p_u=Puntos_Usuarios.objects.filter(identificacion_id=listusuario)
    suma=cantidad_objetos_puntos+puntos
    p_u.update(cantidad=suma)
    return redirect('/puntos/')


#Llamar las bonificaciones con el nombre del usuario de prueba 
def bonificaciones(request, name):
    puntos = Puntos_Usuarios.objects.all().values()
    cantidadp= puntos[0]['cantidad']
    print(cantidadp)
    
    print(name)
    bonificacion=Bonificacion.objects.all().values()
    print(bonificacion)
    print(bonificacion[0])
    bono1=bonificacion[0]
    bono2=bonificacion[1]
    bono3=bonificacion[2]
    bono4=bonificacion[3]
    
    
    return render(request, 'bonificaciones.html', {"name": name, "cantidad":cantidadp, "hood":bono1, "parqueo": bono2, "gym":bono3, "bigos":bono4})

#Hacer la validación del puntaje con la bonificacion a redimir
def redimir(request, name, puntosbono):
    usuario=Usuario.objects.filter(nombre=name)
    listusuario = usuario.values()
    listusuario = listusuario[0]
    listusuario = listusuario['identificacion']
    objeto_puntos = Puntos_Usuarios.objects.filter(identificacion_id=listusuario).values()
    list_objetos_puntos = objeto_puntos[0]
    cantidad_objetos_puntos = list_objetos_puntos['cantidad']
    if(cantidad_objetos_puntos < puntosbono):
        return redirect('/bonificaciones/%s' %(name))
    else:
        o_p = Puntos_Usuarios.objects.filter(identificacion_id=listusuario)
        diferencia = cantidad_objetos_puntos - puntosbono
        o_p.update(cantidad=diferencia)
    return redirect('/bonificaciones/%s' %(name))
