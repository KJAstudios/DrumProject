#include <Arduino.h>

const int numChannels = 6;

// channel to read for single channel data
const int singleChannelReadIndex = 40;

// drum data
const int channels[6] = {A0, A1, A2, A3, A4, A5};
const int maxScanCycles = 4;
int thresholds[6] = {50, 1, 1, 1, 50, 50};
int readInputs[6] = {0, 0, 0, 0, 0, 0};
int peaks[6] = {0, 0, 0, 0, 0, 0};
unsigned int scanTimes[6] = {0, 0, 0, 0, 0, 0};
unsigned int scanCycles[6] = {0, 0, 0, 0, 0, 0};
const String channelNames[6] = {"snare", "snareRim", "c2", "r2", "bass", "c4"};

// highhat switch data
const int highHatPin = 3;
int switchState = 0;
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Serial started");
  pinMode(highHatPin, INPUT);
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

void PrintChannelData(int index)
{
  Serial.println(channelNames[index]);
  Serial.println(peaks[index]);
}

void ClearChannel(int channel)
{
  peaks[channel] = 0;
  scanCycles[channel] = 0;
  scanTimes[channel] = 0;
}

void IncrementTimer(int channel)
{
  scanCycles[channel]++;
  scanTimes[channel] = millis() + 1;
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

void ScanChannel(int curChannel)
{
  ReadChannel(curChannel);

  if (scanCycles[curChannel] <= maxScanCycles && millis() >= scanTimes[curChannel])
  {
    CheckPeak(curChannel);
    IncrementTimer(curChannel);
  }
  else if (scanCycles[curChannel] > maxScanCycles)
  {
    SendToSerial(curChannel);
  }
}

void DrumMainNoBlock()
{
  for (int curChannel = 0; curChannel < numChannels; curChannel++)
  {
    ScanChannel(curChannel);
  }
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

void loop()
{
  // SingleChannelRead();
  // DrumMain();
  DrumMainNoBlock();
}