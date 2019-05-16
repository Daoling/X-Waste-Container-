const int DIRPin = D6; //define Direction pin
const int PULPin = D5; //define Pulse pin
const int TrigPin = D8; //define Direction pin
const int EchoPin = D7; //define Pulse pin

String comdata = "";

void setup()
{
    Serial.begin(115200);
    pinMode (PULPin, OUTPUT);
    pinMode (DIRPin, OUTPUT);
    pinMode (TrigPin, OUTPUT);
    pinMode (EchoPin, INPUT);
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
            Serial.print(TestHigh(), DEC);
            Serial.print("yes");
            }
        else if (!comdata.compareTo("{\"Action\": \"OpenDoor\", \"Number\": \"01\"}")){
          for(int i = 0; i < 32 * 8; i++){
            StepperMotor(false, true, 200);
            }
          //Serial.print("{\"Action\": \"OpenDoor\", \"Number\": \"01\", \"info\": 1}");
          }
        else if (!comdata.compareTo("{\"Action\": \"CloseDoor\", \"Number\": \"01\"}")){
          for(int i = 0; i < 32 * 8; i++){
            StepperMotor(false, false, 200);
            }
          }
        else;
        comdata = "";
    }
}

//步进电机子函数
//函数：StepperMotor    功能：控制步进电机是否脱机、方向、步数
//参数：ENA---脱机状态，true为脱机
//      DIR---方向控制
//      steps---步进的步数，若steps为0，则电机上电电磁锁死，不转
//无返回值
void StepperMotor(boolean ENA, boolean DIR, int steps)
{
  digitalWrite(DIRPin, DIR);
  for (int i = 0; i < steps; i++) //Forward XXXX steps
  {
    digitalWrite(PULPin, HIGH);
    delayMicroseconds(15);
    digitalWrite(PULPin, LOW);
    delayMicroseconds(15);
  }
}

float TestHigh()
{
  float cm;

  digitalWrite(TrigPin, LOW); //低高低电平发一个短时间脉冲去TrigPin
  delayMicroseconds(2);
  digitalWrite(TrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(TrigPin, LOW);
  cm = pulseIn(EchoPin, HIGH) / 58; //将回波时间换算成cm
  return cm;
}
