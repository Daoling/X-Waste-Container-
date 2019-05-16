const int DIRPin = D6; //define Direction pin
const int PULPin = D5; //define Pulse pin

String comdata = "";


void setup() {
  // put your setup code here, to run once:
    Serial.begin(115200);
    pinMode (PULPin, OUTPUT);
    pinMode (DIRPin, OUTPUT);
    digitalWrite(DIRPin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
    while (Serial.available() > 0) {
        comdata += char(Serial.read());
        delay(2);
    }
    if (comdata.length() > 0) {
      if(!comdata.compareTo("test")){
        digitalWrite(DIRPin, HIGH);
        for (int i = 0; i < 6400 * 1; i++) {
          digitalWrite(PULPin, HIGH);
          delayMicroseconds(50);
          digitalWrite(PULPin, LOW);
          delayMicroseconds(50);
          yield();
        }
      }
      if(!comdata.compareTo("past")){
        digitalWrite(DIRPin, LOW);
        for (int i = 0; i < 6400 * 1; i++) {
          digitalWrite(PULPin, HIGH);
          delayMicroseconds(50);
          digitalWrite(PULPin, LOW);
          delayMicroseconds(50);
          yield();
        }
      }
    }
    comdata = "";
}
