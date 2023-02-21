#include <Arduino.h>

const int numChannels = 6;

// drum data
const int channels[6] = {A0, A1, A2, A3, A4, A5};
int thresholds[6] = {25, 1, 1, 1, 1, 1};
int readInputs[6] = {0, 0, 0, 0, 0, 0};
const String channelNames[6] = {"snare", "snareRim", "c2", "r2", "bass", "c4"};

// highhat switch data
const int highHatPin = 3;
int switchState = 0;
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9000);
  Serial.println("Serial started");
  pinMode(highHatPin, INPUT);
}

void loop()
{
  // put your main code here, to run repeatedly:

  for (int i = 0; i < numChannels; i++)
  {
    readInputs[i] = analogRead(channels[i]);
    if (readInputs[i] >= thresholds[i])
    {
      Serial.println(channelNames[i]);
    }
  }
}
