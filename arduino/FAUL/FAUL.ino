int data;
int color;
int val;
int itsred;
int itsred2;
#define REDPIN 5
#define REDPOT 0
#define GREENPIN 6
#define GREENPOT 1
#define BLUEPIN 3
#define BLUEPOT 2


void setup() { 
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  pinMode(REDPIN, OUTPUT);
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);
  digitalWrite (LED_BUILTIN, LOW);
  //Serial.println("Hi!, i see you!");
  String itsred = "Red ";

  
}



 
void loop() {

  int redval = analogRead(REDPOT);
  redval = redval / 4;
  Serial.println("red=" + String(redval)); 

  int greenval = analogRead(GREENPOT);
  greenval = greenval / 4;

  Serial.println("green=" + String(greenval));
//  Serial.println("green=" + REDPOT);
  int blueval = analogRead(BLUEPOT);
  blueval = blueval / 4;
  Serial.println("blue=" + String(blueval));
 // Serial.println("blue=" + REDPOT);










  
while (Serial.available()){
  Serial.setTimeout(2);
  color = Serial.parseInt();
  Serial.read();
  Serial.println("read");
while(Serial.available() == 0){}

  Serial.setTimeout(3);
  val = (Serial.parseInt());
  Serial.read();


}


if (color == 1){
color = 0;
analogWrite (REDPIN, val);
//Serial.println("Red set ");
}else

if (color == 2) {
color = 0;
analogWrite (GREENPIN, val);
//Serial.println("Blue set");
}else
if (color == 3){
color = 0;
analogWrite (BLUEPIN, val);
//Serial.println("Green set ");
}

}
