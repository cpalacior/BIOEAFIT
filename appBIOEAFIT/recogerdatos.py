import  serial # Libreria para obtener datos del arduino
import  time   # Librerir para manejo del tiempo y la hora del sistema
from    datetime import datetime, timedelta
from models import Usuario, Puntos_Usuarios, Bonificacion

puerto = 'COM7'

def mainApp():
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
            
            print("Dato #"+str(i+1))
            print("------------------------")
            leer_datos(list_in_floats)               # Llamo la función de lectura de datos on un argumento de la lista donde guardo los datos 
            verificarUsuario(list_in_floats)         # Mostrando los datos por el monitor
            print("Fin")
            break

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
    
def verificarUsuario(list_in_floats):
    idusuario = list_in_floats[0]
    print(idusuario)
    usuario = Usuario.objects.get(identificacion = idusuario)
    print(usuario)

def visualizar_datos(list_in_floats):
    peso = list_in_floats[0]
    distancia = list_in_floats[1]
    #TemperaturaF = list_in_floats[2]
    #IndiceCalorC = list_in_floats[3]
    #IndiceCalorF = list_in_floats[4]
    print('Peso en gr:'+str(peso))
    print('Distancia en cm:'+str(distancia))
    #print('Humedad:'+str(Humedad))
    #print('Indice de calor oC:'+str(IndiceCalorC))
    #print('Indice de Calor oF:'+str(IndiceCalorF))
    print("------------------------")

if __name__ == '__main__':
    mainApp()