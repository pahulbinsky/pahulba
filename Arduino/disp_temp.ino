#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>
#include <Wire.h>
U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C u8g2(U8G2_R0); 
#include <dht11.h>
dht11 sensor;
#define DHT11PIN 4

void setup(void) {
   u8g2.begin();
}
void loop(void) {
  for (int x = 0; x <= 100; x++)

{
   u8g2.clearBuffer();
   u8g2.setFont(u8g2_font_logisoso28_tr);
   u8g2.print("Humidity (%): ");


   u8g2.print("Temperature (C): ");
   
   delay(10);
  }
}
