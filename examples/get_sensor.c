#include <Wire.h>
#define ADXL 0x1D                                       //Datasheet pages 4 and 7 have info that will be necessary for future development. 

void setup() {
  Wire.begin();                                         // initiate the accelerometer   
  Wire.setClock(3400000L);
  Serial.begin(128000);                                   // initiate the serial monitor  
  delay(100);   
  Wire.beginTransmission(ADXL);                         //set STBY bit 0 to low / turn on MEASURE mode 
  Wire.write(0x2D);   
  Wire.write(0x00);   
  Wire.endTransmission();  
  delay(100); 
  Wire.beginTransmission(ADXL);                         //set RANGE to +/- 2g  pg. 37 of data sheet
  Wire.write(0x2C);   
  Wire.write(0x01);   
  Wire.endTransmission(); 
  delay(100);
  Wire.beginTransmission(ADXL);                         //set data rate to 4000HZ page 37 
  Wire.write(0x28);
  Wire.write(0x00);
  Wire.endTransmission();
  delay(100);
}

