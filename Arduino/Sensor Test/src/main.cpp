#include <Arduino.h>
#include <Servo.h> 
#include <SPI.h>
#include "Ucglib.h"           
#define  trigPin   6 
#define  echoPin   5  
#define  ServoPin  3
#define VRx A0
int Ymax = 128;
int Xmax = 160;
int Xcent = Xmax / 2;
int base = 118;
int scanline = 105;
Servo baseServo; 
Ucglib_ST7735_18x128x160_HWSPI ucg(9,10,8);

void cls()
{
  ucg.setColor(0, 0, 0, 0);
  for(int s=0;s<128;s+=8)
  {
    for(int t=0;t<160;t+=16)
    {
      ucg.drawBox(t,s,16,8);
    } 
  }
}

void fix()
{
  int radii[] = {115,86,58,29};
  ucg.setColor(0, 40, 0);
  ucg.drawDisc(Xcent, base+1, 3, UCG_DRAW_ALL); 
  for (int r : radii)
  {
    ucg.drawCircle(Xcent, base+1, r, UCG_DRAW_UPPER_LEFT);
    ucg.drawCircle(Xcent, base+1, r, UCG_DRAW_UPPER_RIGHT);
  }
  ucg.drawLine(0, base+1, Xmax,base+1);

  int disRadii[] = {15,32,60,89};
  int dis[] = {100,75,50,25};

  ucg.setColor(0, 180, 0);
  for (int i = 0; i < 4; i++)
  {
    ucg.setPrintPos(70,disRadii[i]);
    ucg.print(dis[i]);
    ucg.print("cm");
  }
}

void setup(void)
{
  ucg.begin(UCG_FONT_MODE_SOLID);
  ucg.setRotate90();
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
  baseServo.attach(ServoPin);

  ucg.setFont(ucg_font_orgv01_hr);
  ucg.setFontMode(UCG_FONT_MODE_TRANSPARENT);
  ucg.setColor(0, 0, 100, 0);
  ucg.setColor(1, 0, 100, 0);
  ucg.setColor(2, 20, 20,20);
  ucg.setColor(3, 20, 20, 20);
  ucg.drawGradientBox(0, 0, 160, 128);
  ucg.setPrintDir(0);
  ucg.setColor(0, 5, 0);
  ucg.setPrintPos(27,42);
  ucg.setFont(ucg_font_logisoso18_tf);  
  ucg.print("Mini Radar");
  ucg.setColor(0, 255, 0);
  ucg.setPrintPos(25,40);
  ucg.print("Mini Radar");
  ucg.setFont(ucg_font_helvB08_tf);
  ucg.setColor(0, 255, 0);
  ucg.setPrintPos(40,100);
  ucg.print("Testing...");
  ucg.setColor(0, 255, 0);

  for(int x=-180;x<180;x+=5)
  { 
    baseServo.write(x);
    delay(50);
  }

  baseServo.write(0);
  ucg.print("OK!");
  delay(500);
  for (int i = 0; i < 4; i++)
  {
    ucg.setColor(i,0,0,0);
  }
  cls();
  fix();
}


int getDistance()
{ 
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return (duration*0.034)/2.0;
}

float lastAngleRad = 0;
float lastTime = 0;

void loop(void)
{
  int xValue = analogRead(VRx);
  int currentAngle = map(xValue, 0, 1023, 0, 180);
  currentAngle = constrain(currentAngle, 0, 180);
  baseServo.write(currentAngle);

  float rad = radians(currentAngle);

  ucg.setColor(0,0,0);
  ucg.drawLine(
    Xcent, 
    base, 
    scanline * cos(lastAngleRad) + Xcent,
    base - scanline * sin(lastAngleRad)
  );

  ucg.setColor(0,255,0);
  ucg.drawLine(
    Xcent, 
    base, 
    scanline * cos(rad) + Xcent,
    base - scanline * sin(rad)
  );

  if(lastAngleRad != rad) fix();

  float distance = getDistance();

  if (distance < 100)
  {
    ucg.setColor(255,0,0);
    ucg.drawDisc(1.15 * distance * cos(rad)+Xcent,-(1.15*distance*sin(rad))+base,1,UCG_DRAW_ALL);
  } 
  else 
  {
    ucg.setColor(255,255,0);
    ucg.drawDisc(116*cos(rad)+Xcent,-116*sin(rad)+base,1,UCG_DRAW_ALL);
  }

  lastAngleRad = rad;

  lastTime = (micros() - lastTime);

  Serial.print(millis()/1000.0,2);
  Serial.print(",");
  Serial.print(lastTime);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(",");
  Serial.println(currentAngle);
}