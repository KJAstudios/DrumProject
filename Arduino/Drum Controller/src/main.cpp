#include <Arduino.h>
#include "main.h"

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Serial started");
  pinMode(highHatPin, INPUT);
}

void loop()
{
  CheckForInput();
  // SingleChannelRead();
  // DrumMain();
  DrumMainNoBlock();
}

void CheckForInput()
{
  if (Serial.available())
  {
    String fullCommand = Serial.readStringUntil('\r');
    Serial.println("command Received: " + fullCommand);
    int splitIndex = fullCommand.indexOf(':');
    String command = fullCommand.substring(0, splitIndex);

    if (command == "scanTime")
    {
      String value = fullCommand.substring(splitIndex + 1, fullCommand.length());
      int newScanTime = value.toInt();
      maxScanCycles = newScanTime;
      Serial.print("New Scan Time: ");
      Serial.println(maxScanCycles);
      return;
    }

    else if(command == "threshold"){
      String values = fullCommand.substring(splitIndex + 1, fullCommand.length());
      int valueSplit = values.indexOf(':');
      String channelName = values.substring(0, valueSplit);
      String thresholdText = values.substring(valueSplit + 1, values.length());
      int channelIndex = channelName.toInt();
      int newThreshold = thresholdText.toInt();

      thresholds[channelIndex] = newThreshold;

      Serial.print("New Threshold: ");
      Serial.print(thresholds[channelIndex]);
      Serial.print(" for channel ");
      Serial.println(channelIndex);
    }
  }
}

void DrumMainNoBlock()
{
  for (int curChannel = 0; curChannel < numChannels; curChannel++)
  {
    ScanChannel(curChannel);
  }
}

void ScanChannel(int curChannel)
{
  ReadChannel(curChannel);

  if (scanCycles[curChannel] <= maxScanCycles && millis() >= currentScanTimes[curChannel])
  {
    CheckPeak(curChannel);
    IncrementTimer(curChannel);
  }
  else if (scanCycles[curChannel] > maxScanCycles)
  {
    SendToSerial(curChannel);
  }
}

void ReadChannel(int index)
{
  readInputs[index] = analogRead(channels[index]);
}

void CheckPeak(int index)
{
  if (readInputs[index] > peaks[index])
  {
    peaks[index] = readInputs[index];
  }
}

void IncrementTimer(int channel)
{
  scanCycles[channel]++;
  currentScanTimes[channel] = millis() + 1;
}

void SendToSerial(int curChannel)
{
  if (peaks[curChannel] > thresholds[curChannel])
  {
    PrintChannelData(curChannel);
    ClearChannel(curChannel);
  }
  else
  {
    ClearChannel(curChannel);
  }
}

void PrintChannelData(int index)
{
  Serial.print(channelNames[index] + " ");
  Serial.println(peaks[index]);
}

void ClearChannel(int channel)
{
  peaks[channel] = 0;
  scanCycles[channel] = 0;
  currentScanTimes[channel] = 0;
}

void SingleChannelRead()
{
  int readInput = analogRead(singleChannelReadIndex);
  if (readInput > 0)
  {
    Serial.println(readInput);
  }
}

void DrumMain()
{
  /*
TODOS
add better peak detection
add a scan range that checks over a set number of ms for a peak
if the peak is above the threshold, then send the serial out
*/
  for (int curChannel = 0; curChannel < numChannels; curChannel++)
  {
    ReadChannel(curChannel);

    if (readInputs[curChannel] >= thresholds[curChannel])
    {
      for (int curScan = 0; curScan < maxScanCycles; curScan++)
      {

        delay(1);

        ReadChannel(curChannel);

        CheckPeak(curChannel);

        if (readInputs[curChannel] < peaks[curChannel])
        {
          delay(maxScanCycles - curScan);
          break;
        }
      }

      if (peaks[curChannel] >= thresholds[curChannel])
      {
        PrintChannelData(curChannel);
      }

      peaks[curChannel] = 0;
    }
  }
}