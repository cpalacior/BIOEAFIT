from django.shortcuts import render, redirect
from .models import Usuario, Puntos_Usuarios, Bonificacion, TipoUsuario
import serial  # Libreria para obtener datos del arduino
import time   # Librerir para manejo del tiempo y la hora del sistema
import cv2  # Libreria para el reconocimiento de la botella 

puerto = 'COM7'

# Llamar inicio
def inicio(request):
    return render(request, 'inicio.html')

def inicio1(request, mensaje, puntos):
    return render(request, 'inicio.html', {"mensaje": mensaje, "cantidad": puntos})

# Llamar las bonificaciones con el nombre del usuario de prueba
def bonificaciones(request, name):
    user = Usuario.objects.filter(nombre = name).values()[0]
    idpuntos = user["identificacion"]
    user = user["nombre"]
    puntos = Puntos_Usuarios.objects.filter(identificacion_id = idpuntos).values()
    cantidadp = puntos[0]['cantidad']
    print(cantidadp)
    print(name)
    bonificacion = Bonificacion.objects.all()

    return render(request, 'bonificaciones.html', {"name": user, "cantidad": cantidadp, "bono": bonificacion})

# Hacer la validación del puntaje con la bonificacion a redimir
def redimir(request, name, puntosbono):
    usuario = Usuario.objects.filter(nombre=name)
    listusuario = usuario.values()
    listusuario = listusuario[0]
    listusuario = listusuario['identificacion']
    objeto_puntos = Puntos_Usuarios.objects.filter(
        identificacion_id=listusuario).values()
    list_objetos_puntos = objeto_puntos[0]
    cantidad_objetos_puntos = list_objetos_puntos['cantidad']
    if (cantidad_objetos_puntos < puntosbono):
        return redirect('/bonificaciones/%s' % (name))
    else:
        o_p = Puntos_Usuarios.objects.filter(identificacion_id=listusuario)
        diferencia = cantidad_objetos_puntos - puntosbono
        o_p.update(cantidad=diferencia)
    return redirect('/bonificaciones/%s' % (name))


def puntos1(request):
    # Defino una variable tipo arrglo para guardar los datos que lea
    list_in_floats = []
    while True:
        try:
            cantDatos = 1  # Captura la cantidad de datos que quiero capturar
        except ValueError:
            print("Error: no es un valor numerico")
        except:
            print("Error: no se ha ingresado datos")
        else:
            print("Procesando...")
            print("------------------------")
            print("Dato 1")
            print("------------------------")
            # Llamo la función de lectura de datos on un argumento de la lista donde guardo los datos
            claseObjeto = DetectarBotella()
            time.sleep(1)
            leer_datos(list_in_floats)
            try:
                idusuario = round(list_in_floats[0])
                print(idusuario)
                usuario = Usuario.objects.get(identificacion=idusuario)
                print(usuario)
                print(list_in_floats[1])
                puntos = float(list_in_floats[1])
                puntos = round(puntos)
                puntos_usuario = Puntos_Usuarios.objects.filter(identificacion_id = idusuario)
                
                cantidadp = puntos_usuario.values()[0]
                
                cantidadp = cantidadp["cantidad"]
                
                suma = cantidadp + puntos
                
                if claseObjeto != 44 or claseObjeto != 11 or claseObjeto != 70 or claseObjeto != 86:
                    restarPuntos(idusuario, suma)
                    return redirect('/inicio1/trampa/%s' %(puntos))
                puntos_usuario.update(cantidad=suma)
                return redirect('/inicio1/success/%s' %(puntos))
            except:
                print("No existe este usuario")
                idusuario = list_in_floats[0]
                idusuario = round(idusuario)
                # Mostrando los datos por el monitor
                return redirect('/inicio1/error/%s' %(idusuario))

def leer_datos(list_in_floats):
    list_values = []
    arduino = serial.Serial(puerto, 9600)
    time.sleep(5)
    print("Ponle el peso")
    arduino_data = arduino.readline()
    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('|')
    for item in list_values:
        list_in_floats.append(float(item))
    arduino_data = 0
    arduino.close()

def DetectarBotella():
    cap = cv2.VideoCapture('http://192.168.1.101:8080/video')
    time.sleep(1)
    classNames= []
    classFile = 'C:/Users/USER/Documents/Camilo/programacion/PI1/proyecto/BIOEAFIT/Detector/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    configPath = 'C:/Users/USER/Documents/Camilo/programacion/PI1/proyecto/BIOEAFIT/Detector/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'C:/Users/USER/Documents/Camilo/programacion/PI1/proyecto/BIOEAFIT/Detector/frozen_inference_graph.pb'
    net= cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5,127.5,127.5))
    net.setInputSwapRB(True)
    contador = 0
    for i in range(5): 
        if i == 4:
            return classIds
    
        seccess,img = cap.read()
        classIds, confs, bbox = net.detect(img,confThreshold=0.5)
        print(classIds,bbox)
        if len(classIds) != 0:
            classIds = classIds[0]
            try:
                if(classIds == 44):
                    print("Botella aaaaaa")
            except:
                pass
            for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                cv2.rectangle(img,box,color=(0,255,0),thickness=3)
                cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) 
        cv2.imshow("Output",img)
        cv2.waitKey(1)
        contador = contador + 1
    cv2.destroyAllWindows("Output") 

def restarPuntos(identificacion, valor):
    puntos_usuario = Puntos_Usuarios.objects.filter(identificacion_id = identificacion)
    cantidadp = puntos_usuario.values()[0]
    cantidadp = cantidadp["cantidad"]
    if valor > cantidadp:
        resta = 0
    else:
        resta = cantidadp - valor
    puntos_usuario.update(cantidad=resta)

def informacion(request):
    return render(request, 'informacion.html')

def informacion1(request, name):
    return render(request, 'informacion.html', {"name": name})

def signin(request):
    formulario = request.POST.dict()
    print(formulario)
    if request.method == 'POST':
        try:
            user = Usuario.objects.filter(
            correo=formulario["correo"]).filter(clave=formulario["clave"])
            tipouser = user.values()[0]
            nombreuser = tipouser["nombre"]
            tipouser = tipouser["idtipousuario_id"]
            if tipouser == 2:
                return redirect('/administrador/')
            return redirect('/inicioUser/%s' %(nombreuser))
        except:
            return redirect('/signin/%s' % ("error"))
    return render(request, 'login.html')

def signinMalo(request, mensaje):
    formulario = request.POST.dict()
    print(formulario)
    if request.method == 'POST':
        try:
            user = Usuario.objects.filter(
            correo=formulario["correo"]).filter(clave=formulario["clave"])
            tipouser = user.values()[0]
            nombreuser = tipouser["nombre"]
            tipouser = tipouser["idtipousuario_id"]
            if tipouser == 2:
                return redirect('/administrador/')
            return redirect('/inicioUser/%s' %(nombreuser))
        except:
            return redirect('/signin/%s' % ("error"))
    return render(request, 'login.html', {"alerta":mensaje})


def registro(request):
    formulario = request.POST.dict()
    print(formulario)
    T1 = TipoUsuario.objects.get(idtipousuario=request.POST['idtipousuario'])
    usuario = Usuario(identificacion=formulario['identificacion'], nombre=formulario['nombre'].strip(), correo=formulario['correo'].strip(), clave=formulario['clave'].strip(), direccion=formulario['direccion'], edad=formulario['edad'], telefono=formulario['telefono'], idtipousuario=T1)
    usuario.save()
    usuario1 = Usuario.objects.filter(
        identificacion=formulario['identificacion']).values()
    usuario1 = usuario1[0]
    puntosU = Puntos_Usuarios(
        identificacion_id=usuario1['identificacion'], cantidad=0)
    puntosU.save()
    print(formulario)
    return redirect('/')

def administrador(request):
    usuarios = Usuario.objects.filter(idtipousuario_id=1)
    return render(request, 'admin.html', {"usuarios": usuarios})

def editar(request):
    formulario = request.POST.dict()
    print("editando")
    print(formulario)
    usuario = Usuario.objects.filter(identificacion = formulario["identificacion"])
    usuario.update(identificacion = formulario["identificacion"], nombre = formulario["nombre"].strip(), correo = formulario["correo"].strip(), clave = formulario["clave"].strip(), direccion = formulario["direccion"], edad = formulario["edad"], telefono = formulario["telefono"])
    return redirect("/administrador/")

def editarBonos(request):
    formulario = request.POST.dict()
    print("editando")
    print(formulario)
    bonificacion = Bonificacion.objects.filter(nombre = formulario["nombre"])
    bonificacion.update(nombre = formulario["nombre"], valor = formulario["valor"], imagen = formulario["imagen"], descripcion = formulario["descripcion"])
    return redirect("/adminBonos/")

def registroadministrador(request):
    formulario = request.POST.dict()
    print(formulario)
    T1 = TipoUsuario.objects.get(idtipousuario=request.POST['idtipousuario'])
    usuario = Usuario(identificacion=formulario['identificacion'], nombre=formulario['nombre'].strip(), correo=formulario['correo'].strip(), clave=formulario['clave'].strip(), direccion=formulario['direccion'], edad=formulario['edad'], telefono=formulario['telefono'], idtipousuario=T1)
    usuario.save()
    usuario1 = Usuario.objects.filter(
        identificacion=formulario['identificacion']).values()
    usuario1 = usuario1[0]
    puntosU = Puntos_Usuarios(
        identificacion_id=usuario1['identificacion'], cantidad=0)
    puntosU.save()
    print(formulario)
    return redirect('/administrador/')

def eliminarStudent(request, name):
    user = Usuario.objects.filter(nombre = name)
    puntos_usuario = user.values()[0]
    puntos_usuario = puntos_usuario["identificacion"]
    puntos = Puntos_Usuarios.objects.filter(identificacion_id = puntos_usuario)
    puntos.delete()
    user.delete()
    return redirect("/administrador/")

def adminBonos(request):
    formulario = request.POST.dict()
    print(formulario)
    if request.method == 'POST':
        bonificacion = Bonificacion(
            nombre=formulario['nombre'], valor=formulario['valor'], imagen=formulario['imagen'], descripcion=formulario['descripcion'])
        bonificacion.save()
    bonos = Bonificacion.objects.all()
    return render(request, 'adminBonos.html', {"bonos": bonos})

def eliminarBonos(request, name):
    bono = Bonificacion.objects.filter(nombre = name)
    bono.delete()
    return redirect("/adminBonos/")

def inicioUser(request, name):
    usuarios = Usuario.objects.filter(nombre = name)
    nombreusuario = usuarios.values()
    nombreusuario = nombreusuario[0]
    return render(request, 'inicioUsuario.html', {"name": nombreusuario["nombre"]})

def signout(request):
    return redirect('/')