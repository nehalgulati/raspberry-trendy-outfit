#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

#define PIN            3
#define NUMPIXELS      4


int Tx = 10;
int Rx = 11;

SoftwareSerial bluetooth(Tx, Rx);

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);


int analogPin = 3;     
int data = 0;           

int value=0;
int numList = 3;
int dataList[2];

int r_value = 0;
int g_value = 0;
int b_value = 0;

void setup(){
  Serial.begin(9600);   
  Serial.println("Arduino is ready");
  pixels.begin();
}

void loop(){
  while (Serial.available()>0){
    for (int j=0;j<numList;j++){
      dataList[j] = Serial.read();
      r_value = (int)dataList[0];
      g_value = (int)dataList[1];
      b_value = (int)dataList[2];

      for(int i=0;i<NUMPIXELS;i++){
        pixels.setPixelColor(i, pixels.Color(r_value,g_value,b_value)); //RGB every 3 values to mapped
        pixels.show();
        delay(10);
      }
    }
  }
}
