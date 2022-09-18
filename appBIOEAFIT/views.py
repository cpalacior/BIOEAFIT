from pipes import Template
from pydoc import doc
from xml.dom.minidom import Document
from django.shortcuts import render, redirect
from .models import Usuario, Puntos_Usuarios, Bonificacion
import  serial # Libreria para obtener datos del arduino
import  time   # Librerir para manejo del tiempo y la hora del sistema
from    datetime import datetime, timedelta

puerto = 'COM7'

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
    puntos = (float(request.POST['peso'])+float(request.POST['tamanio']))/(20+float(request.POST['calidad']))
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
    bonificacion=Bonificacion.objects.all()
    
    
    return render(request, 'bonificaciones.html', {"name": name, "cantidad":cantidadp, "bono":bonificacion})

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

def puntos1(request):
    list_in_floats = []                # Defino una variable tipo arrglo para guardar los datos que lea
    while True:
        try:
            cantDatos = 1 #Captura la cantidad de datos que quiero capturar
        except ValueError:
            print("Error: no es un valor numerico")
        except:
            print("Error: no se ha ingresado datos")
        else:
            print("Procesando...")
            print("------------------------")
            
            print("Dato 1")
            print("------------------------")
            leer_datos(list_in_floats)               # Llamo la función de lectura de datos on un argumento de la lista donde guardo los datos 
            try:
                idusuario = list_in_floats[0]
                print()

                print(idusuario)
                usuario = Usuario.objects.get(identificacion = idusuario)
                print(usuario)
                print(list_in_floats[1])
                print(list_in_floats[2])
                print(list_in_floats[3])
                
                usuarios = Usuario.objects.all()
                nombreusuario = usuarios.values("nombre")
                nombreusuario = nombreusuario[0]
                puntos = Puntos_Usuarios.objects.all()
                cantidadp = puntos.values("cantidad")
                cantidadp= cantidadp[0]

                tamanio = 30- list_in_floats[1]
                return render(request, 'puntos.html', {"name": nombreusuario["nombre"], "cantidad": cantidadp["cantidad"], "tamanio": tamanio, "peso": list_in_floats[2], "calidad": list_in_floats[3]})
            except:
                print("No existe este usuario")
                return redirect('/inicio')        # Mostrando los datos por el monitor


def verificarUsuario(list_in_floats):
    try:
        idusuario = list_in_floats[0]
        print()
        
        print(idusuario)
        usuario = Usuario.objects.get(identificacion = idusuario)
        print(usuario)
        print(list_in_floats[1])
        print(list_in_floats[2])
        print(list_in_floats[3])
    except:
        print("No existe este usuario")
        return redirect('/inicio')

def leer_datos (list_in_floats):
    list_values = []
    arduino = serial.Serial(puerto, 9600)
    arduino_data = arduino.readline()
    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('|')
    for item in list_values:
        list_in_floats.append(float(item))
    arduino_data = 0
    arduino.close()