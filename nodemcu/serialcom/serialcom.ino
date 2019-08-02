const int DIRPin = D6; //define Direction pin
const int PULPin = D5; //define Pulse pin
String comdata = "";

void setup()
{
    Serial.begin(115200);
    pinMode (PULPin, OUTPUT);
    pinMode (DIRPin, OUTPUT);
}

void loop()
{
    while (Serial.available() > 0)  
    {
        comdata += char(Serial.read());
        delay(2);
    }
    if (comdata.length() > 0)
    {
        if(!comdata.compareTo("{\"Action\": \"OpenDoor\", \"Number\": \"01\"}")){
            digitalWrite(DIRPin, LOW);
            for (int i = 0; i < 6400 * 2; i++) {
              digitalWrite(PULPin, HIGH);
              delayMicroseconds(50);
              digitalWrite(PULPin, LOW);
              delayMicroseconds(50);
              yield();
              }
            Serial.print("{\"Action\": \"OpenDoor\", \"Number\": \"01\", \"info\": 1}");
            }
        else if(!comdata.compareTo("{\"Action\": \"CloseDoor\", \"Number\": \"01\"}")){
          digitalWrite(DIRPin, HIGH);
          for (int i = 0; i < 6400 * 2; i++) {
            digitalWrite(PULPin, HIGH);
            delayMicroseconds(50);
            digitalWrite(PULPin, LOW);
            delayMicroseconds(50);
            yield();
            }
          Serial.print("{\"Action\": \"CloseDoor\", \"Number\": \"01\", \"info\": 1}");
          }
        else{Serial.print("unknow");}
        comdata = "";
    }
}
