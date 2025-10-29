#include <Arduino.h>
#include <Servo.h>

const int trigPin = 9;
const int echoPin = 10;

const int VRx = A0;
//const int VRy = A1;
//const int SW = 2;

int xValue = 0;
int yValue = 0;
int buttonState = 0;

long duration;
float distanceCm;

long lastTime = 0;

Servo scanner;

void setup() 
{
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  scanner.attach(6); 
  scanner.write(0);
  lastTime = micros();
}

float getDistance() 
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return (duration * 0.034) / 2.0;
}

int angle = 0;

void loop() 
{

  xValue = analogRead(A0);
  angle = map(xValue, 0, 1023,0,180);
  scanner.write(angle);
  delay(60);

  float distance = getDistance();
  lastTime = (micros() - lastTime);
  
  Serial.print(millis()/1000);
  Serial.print(",");
  Serial.print(lastTime);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(",");
  Serial.println(angle);
}