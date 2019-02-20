//本次实验电机驱动采用共阴极接线方式
//将步进电机的参数写到一个子函数中，并加入限位开关，触动限位开关可实现步进电机停转
//20180519 by xcx
const int DIRPin = D1; //define Direction pin
const int PULPin = D0; //define Pulse pin
 
void setup()
{
  pinMode (PULPin, OUTPUT);
  pinMode (DIRPin, OUTPUT);
  digitalWrite(DIRPin, true);
}
 
void loop()
{
    digitalWrite(PULPin, HIGH);
    delayMicroseconds(200);
    digitalWrite(PULPin, LOW);
    delayMicroseconds(200);
  //StepperMotor(false, true, 3200);//此时3200由于在这个循环中，只要不修改成0，则修改他的值没什么影响，转速不会改变

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
    delayMicroseconds(500);
    digitalWrite(PULPin, LOW);
    delayMicroseconds(500);
  }
}
