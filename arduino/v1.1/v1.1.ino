int data;
int color;
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
  digitalWrite (LED_BUILTIN, LOW);
  Serial.println("Hi!, I am Arduino");



}
 
void loop() {
while (Serial.available()){
  Serial.setTimeout(2);
  color = Serial.parseInt();
}

if (color == 1)
analogWrite (REDPIN, "255");
else
if (color == 2)
analogWrite (BLUEPIN, "255");
else
if (color == 3)
analogWrite (GREENPIN, "255");



}
