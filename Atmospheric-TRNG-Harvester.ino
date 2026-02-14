const int antennaPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int sample1 = analogRead(antennaPin) & 1;
  delayMicroseconds(50);
  int sample2 = analogRead(antennaPin) & 1;

  if (sample1 != sample2) {
    Serial.print(sample1);
  }
}