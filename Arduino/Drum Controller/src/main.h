#include <Arduino.h>

const int numChannels = 6;

// channel to read for single channel data
const int singleChannelReadIndex = 6;

// drum data
const int channels[6] = {A0, A1, A2, A3, A4, A5};
int maxScanCycles = 49;
int thresholds[6] = {50, 1, 1, 1, 50, 50};
int readInputs[6] = {0, 0, 0, 0, 0, 0};
int peaks[6] = {0, 0, 0, 0, 0, 0};
unsigned int currentScanTimes[6] = {0, 0, 0, 0, 0, 0};
int scanCycles[6] = {0, 0, 0, 0, 0, 0};
const String channelNames[6] = {"snare", "snareRim", "c2", "r2", "bass", "c4"};

// highhat switch data
const int highHatPin = 3;
int switchState = 0;

void CheckForInput();
void DrumMain();
void SingleChannelRead();
void DrumMainNoBlock();
void ReadChannel(int index);
void CheckPeak(int index);
void PrintChannelData(int index);
void ClearChannel(int channel);
void IncrementTimer(int channel);
void SendToSerial(int curChannel);
void ScanChannel(int curChannel);