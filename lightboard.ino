int val;
int ch[] = {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 20, 21, 22, 23, 29, 30};
int x = 1;
int chnum = 0;
int chval = 0;
#define ch_count 16
#define multi 1000
#define led 13

void setup() {
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  // set all pins
  while(x <= ch_count) {
    pinMode(ch[x], OUTPUT);
    x++;
  }
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  while(Serial.available()) {
    Serial.setTimeout(3);
    val = (Serial.parseInt());
    Serial.read();
   
    chnum = float(val) / float(multi);
    chval = val % multi;

    analogWrite(ch[chnum], chval);
    
    //Serial.print(chnum);
    //Serial.print("\n");
  }
}
