#include <LCD_I2C.h>
#include <Servo.h>
#include <Keypad.h>
#include <HX711_ADC.h>

//CONSTANTES
#define DOUT A1
#define CLK A0

//VARIABLES
float const ftrCal_ = 231.8885;
float peso = 0;
int i = 0;
float puntos = 0;

HX711_ADC balanza(DOUT, CLK); //HX711 constructor (dout pin, sck pin)
LCD_I2C lcd(0x27, 20, 4); // Default address of most PCF8574 modules, change according
Servo myservo;  // crea el objeto servo

long t;
long t_espera = 1000; //Nota 0: coloquemos este tiempo de espera para que se tomen datos cada 1 segundo (500 milesegundos)
long t_actual;
int pos = 90;

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
  
  myservo.attach(10);  // vincula el servo al pin digital 10
  
  lcd.begin(); 
  lcd.backlight();
  lcd.setCursor(4, 1); lcd.print("Configurando");
  lcd.setCursor(12, 2); lcd.print("pesa");
  
  pinMode(LED_BUILTIN, OUTPUT);
  balanza.begin();
  balanza.start(2000); // la preciscion de la tara puede mejorar al añadir un par de segundos
  balanza.setCalFactor(ftrCal_);
  t_actual = millis();
  lcd.clear();
  lcd.setCursor(3,1);
  lcd.print("Pon la botella");
  lcd.setCursor(5,2);
  lcd.print("en la balanza");
  
  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);

  pinMode(0, INPUT);
  delay(1000);
}

void loop(){
  //Esto es para la identificación
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("Digita tu");
  lcd.setCursor(3, 1);
  lcd.print("identificación");
  lcd.setCursor(4, 2);
  lcd.print("*:reintentar");
  lcd.setCursor(4, 3);
  lcd.print("#:enviar");
  
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
    
   //Esto es para la calidad
   lcd.clear();
  lcd.setCursor(5, 1);
  lcd.print("Digita tu");
  lcd.setCursor(6, 2);
  lcd.print("calidad");
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
 //varia la posicion del servo de 90 a 180 con una espera de 1s
    for (pos = 90; pos <= 180; pos += 1) 
   {
      myservo.write(pos);              
      delay(15);                       
   }
  delay(500);
   //varia la posicion de 180 a 0, con esperas de 15ms
   for (pos = 180; pos >= 90; pos -= 1) 
   {
      myservo.write(pos);              
      delay(15);                       
   }
   delay(500);
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
  puntos = ((peso*-1) + (30 - cm))/(20+input_password1)
  Serial.println(String(input_password) + "|" + String(puntos));
  lcd.clear();
  lcd.setCursor(5,0);
  lcd.print(input_password);
  lcd.setCursor(4,1);
  lcd.print("conseguiste");
  lcd.setCursor(7,2);
  lcd.print(puntos);
  lcd.setCursor(10,2);
  lcd.print("ptos.");
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
