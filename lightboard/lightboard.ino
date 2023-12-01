#include "writefix.h"

static int channelPins[] = {0,3,4,2,6,7,5,9,10,8,20,21,14,23,29,22,30};
static int channelCount = 16;
static int ledPin = 13;

char inputBuffer[256];
unsigned int bufferPosition = 0;

void setup() {
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, HIGH);

    for(int i = 0; i < channelCount; i++) {
        pinMode(channelPins[i], OUTPUT);
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

            if (bufferPosition >= sizeof(inputBuffer) - 1) {
                bufferPosition = sizeof(inputBuffer) - 1;
                Serial.printf("ERROR: Input buffer overflow: %s\n", inputBuffer);
            }
        }
    }
}

int processCommand(char* command) {
    switch(command[0]) {
        case 's':
            setChannel(command + 1);
            break;
        default:
            Serial.printf("ERROR: Invalid command: %s\n", command);
            return 1;
    }
    return 0;
}

int setChannel(char* command) {
    int channel;
    int value;
    
    if (sscanf(command, "%d:%d", &channel, &value) == 2) {
        analogWrite(channelPins[channel], value);
    } else {
        return 1;
        Serial.printf("ERROR: setChannel: Invalid syntax: %s\n", command);
    }
    return 0;
}
