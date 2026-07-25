#define MQ2pin (0)

float sensorValue;  // переменная для хранения значения датчика

void setup()
{
  Serial.begin(9600); // настроить последовательный порт на скорость 9600
  Serial.println("Gas sensor warming up!");
  delay(20000);       // дать MQ-2 время для прогрева
}

void loop()
{
  sensorValue = analogRead(MQ2pin); // прочитать аналоговый вход 0
  
  Serial.print("Sensor Value: ");
  Serial.print(sensorValue);
  
  if(sensorValue > 600)
  {
    Serial.print(" | Команда ГАЗЫ!");
  }
  
  Serial.println("");
  delay(500); // подождать 0.5 сек до следующего чтения
}
