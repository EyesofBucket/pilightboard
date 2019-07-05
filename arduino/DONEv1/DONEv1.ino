int data;
#define REDPIN 5
void setup() { 
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  pinMode(REDPIN, OUTPUT); 
  digitalWrite (LED_BUILTIN, LOW);
  
  Serial.println("Hi!, I am Arduino");
}
 
void loop() {
while (Serial.available()){
  Serial.setTimeout(3);
  data = Serial.parseInt();
}

analogWrite (REDPIN, data);

}
