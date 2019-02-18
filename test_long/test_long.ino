float cm;

void setup(){
  Serial.begin(9600);
  pinMode(D2, OUTPUT);
  pinMode(D3, INPUT);
}

void loop(){
  digitalWrite(D2, LOW); //低高低电平发一个短时间脉冲去TrigPin
  delayMicroseconds(2);
  digitalWrite(D2, HIGH);
  delayMicroseconds(10);
  digitalWrite(D2, LOW);
  cm = pulseIn(D3, HIGH) / 58; //将回波时间换算成cm
  cm = (int(cm * 100)) / 100; //保留两位小数
  Serial.print(cm); 
  Serial.print("cm");//串口输出 
  Serial.println();
  delay(1000);
}
