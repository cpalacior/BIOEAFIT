#include <Keypad.h>
float peso; //Numero Random

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
  input_password.reserve(32); // maximum input characters is 33, change if needed
  pinMode(TriggerPin, OUTPUT);
   pinMode(EchoPin, INPUT);

  randomSeed(analogRead(0)); // numeros random para los pesos
  pinMode(0, INPUT);
}

void loop(){
  //Serial.println("Ingrese teclas");
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
 //Serial.println("Acá estamos con sensor");
 for(int i = 0; i < 1; i++){
   cm = ping(TriggerPin, EchoPin);
   //Serial.print("Distancia: ");
   //Serial.println(cm);
   delay(100);
  }
  peso = random(9, 46);
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
