#include <Keypad.h>
#include <HX711_ADC.h>

//CONSTANTES
#define DOUT A1
#define CLK A0

//VARIABLES
float const ftrCal_ = 231.8885;
float peso = 0;
int i = 0;
HX711_ADC balanza(DOUT, CLK); //HX711 constructor (dout pin, sck pin)
long t;
long t_espera = 1000; //Nota 0: coloquemos este tiempo de espera para que se tomen datos cada 1 segundo (500 milesegundos)
long t_actual;

const int EchoPin = 48;
const int TriggerPin = 50;

const int ROW_NUM = 4; //four rows
const int COLUMN_NUM = 3; //three columns
int cm = 0;

char keys[ROW_NUM][COLUMN_NUM] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte pin_rows[ROW_NUM] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte pin_column[COLUMN_NUM] = {5, 4, 3}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM );

const String password = "1034916004"; // change your password here
String input_password;
String input_password1;

void setup(){
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  balanza.begin();
  balanza.start(2000); // la preciscion de la tara puede mejorar al añadir un par de segundos
  balanza.setCalFactor(ftrCal_);
  //Serial.println("Configuración completada...");
  t_actual = millis();
   
  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);

  pinMode(0, INPUT);
}

void loop(){
  //Esto es para la identificación
   while(true){
    char key = keypad.getKey();

  if (key){
    //Serial.println(key);

    if(key == '*') {
      input_password = ""; // clear input password
    } else if(key == '#') {
      break;
    } else {
      input_password += key; // append new character to input password string
    }
  }
 }

 
 //Esto es para el ultraSonido
 for(int i = 0; i < 1; i++){
   cm = ping(TriggerPin, EchoPin);
   //Serial.print("Distancia: ");
   //Serial.println(cm);
   delay(100);
  }

  
  //Esto es para el peso
  while(true){
    balanza.update();
    if (millis() > t_actual + t_espera){
      i++;
      peso = balanza.getData();
      String dato_sensor = String(peso);
      //Serial.print("Peso:");
      //Serial.println(peso_);
      t_actual = millis();
      if( i == 3){
        break;
        }
    }
    }

    
   //Esto es para la calidad
  while(true){
    char key = keypad.getKey();

  if (key){
    //Serial.println(key);

    if(key == '*') {
      input_password1 = ""; // clear input password
    } else if(key == '#') {
      break;
    } else {
      input_password1 += key; // append new character to input password string
    }
  }
 }
  Serial.println(String(input_password) + "|" + String(cm) + "|" + String(peso) + "|" + String(input_password1));
  
}

int ping(int TriggerPin, int EchoPin) {
   long duration, distanceCm;
   
   digitalWrite(TriggerPin, LOW);  //para generar un pulso limpio ponemos a LOW 4us
   delayMicroseconds(4);
   digitalWrite(TriggerPin, HIGH);  //generamos Trigger (disparo) de 10us
   delayMicroseconds(10);
   digitalWrite(TriggerPin, LOW);
   
   duration = pulseIn(EchoPin, HIGH);  //medimos el tiempo entre pulsos, en microsegundos
   
   distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm
   return distanceCm;
}
