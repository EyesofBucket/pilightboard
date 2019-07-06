int val;
int ch[] = {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 20, 21, 22, 23, 29, 30};
int x = 1;
#define ch_count 16
#define subval 1000

void setup() {
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
    //Serial.print("READ\n");
    x = 1;
   
    while(x <= ch_count) {
      val-=subval;
      if(val <= 255 && val >= 0) {
        analogWrite(ch[x], val);
        //Serial.print(x);
        //Serial.print(", ");
        //Serial.print(ch[x]);
        //Serial.print(", ");
        //Serial.print(val);
        //Serial.print("\n");

        x = ch_count;
      }
        if(val < 0) {
        x = ch_count;
      }
      x++;
    }
  }
}
