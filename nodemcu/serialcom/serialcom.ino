String comdata = "";

void setup()
{
    Serial.begin(9600);
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
        if(!comdata.compareTo("‘{“Action”:”OpenDoor”,”Number”:”01”}’")){
            Serial.print("da\"ta");
            }
        else{Serial.print("unknow");}
        comdata = "";
    }
}
