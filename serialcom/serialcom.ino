
String comdata = "";

void setup()
{
    Serial.begin(115200);
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
        if(!comdata.compareTo("get high")){
            Serial.print("data");
            }
        else{Serial.print("unknow");}
        comdata = "";
    }
}
