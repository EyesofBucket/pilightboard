#include <stdio.h>

static int channelPins[] = {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 20, 21, 22, 23, 29, 30};
static int channelCount 16;
static int ledPin 13;

char inputBuffer[16];
int bufferPosition = 0;

void setup() {
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, HIGH);

    for(i = 0; i < channelCount; i++) {
        pinMode(channelPins[x], OUTPUT);
    }

    Serial.begin(9600);
}

void loop() {
    if(Serial.available()) {
        char incomingByte = Serial.read();

        if (incomingByte == '\n') {
            inputBuffer[bufferPosition] = '\0';
            bufferPosition = 0;
            processCommand(inputBuffer);
        } else {
            inputBuffer[bufferPosition++] = incomingByte;
            // Overflow protection
            if (bufferPosition >= sizeof(inputBuffer) - 1) {
                bufferPosition = sizeof(inputBuffer) - 1;
            }
        }
    }
}

void processCommand(char* command) {
    switch(command[0]) {
        case 's':
            setChannel(command + 1);
        default:
            return 1;
    }
    return 0;
}

void setChannel(char* command) {
    int channel;
    int value;
    
    if (sscanf(str, "%d %d", &channel, &value) == 2) {
        analogWrite(ch[chnum], chval);
    } else {
        return 1;
    }
    return 0;
}
