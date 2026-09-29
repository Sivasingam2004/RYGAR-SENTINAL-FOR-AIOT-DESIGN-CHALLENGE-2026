#define MQ2_PIN       A0
#define ACS712_PIN    A1
#define WATER_PIN     A2
#define MQ135_PIN     A3

#define PIR1_PIN      2
#define PIR2_PIN      3
#define PARK1_PIN     4
#define PARK2_PIN     5
#define FLAME_PIN     6
#define BUZZER_PIN    7

#define RELAY_LIGHT   12
#define RELAY_FAN     13

#define RELAY_ON      LOW
#define RELAY_OFF     HIGH

void setup() {
  pinMode(PIR1_PIN, INPUT);
  pinMode(PIR2_PIN, INPUT);
  pinMode(PARK1_PIN, INPUT);
  pinMode(PARK2_PIN, INPUT);
  pinMode(FLAME_PIN, INPUT);

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  pinMode(RELAY_LIGHT, OUTPUT);
  pinMode(RELAY_FAN, OUTPUT);

  digitalWrite(RELAY_LIGHT, RELAY_OFF);
  digitalWrite(RELAY_FAN, RELAY_OFF);

  Serial.begin(9600);

  delay(1000);
  Serial.println("RYGAR NODE 2 ONLINE");
}

void loop() {
  int mq2Value   = analogRead(MQ2_PIN);
  int currentRaw = analogRead(ACS712_PIN);
  int waterValue = analogRead(WATER_PIN);
  int mq135Value = analogRead(MQ135_PIN);

  int pir1  = digitalRead(PIR1_PIN);
  int pir2  = digitalRead(PIR2_PIN);
  int park1 = digitalRead(PARK1_PIN);
  int park2 = digitalRead(PARK2_PIN);
  int flame = digitalRead(FLAME_PIN);

  bool fireDetected = (flame == LOW);

  if (fireDetected)
    digitalWrite(BUZZER_PIN, HIGH);
  else
    digitalWrite(BUZZER_PIN, LOW);

  if (pir1 == HIGH || pir2 == HIGH)
    digitalWrite(RELAY_LIGHT, RELAY_ON);
  else
    digitalWrite(RELAY_LIGHT, RELAY_OFF);

  digitalWrite(RELAY_FAN, RELAY_OFF);

  Serial.print("NODE2,");
  Serial.print("MQ2="); Serial.print(mq2Value);
  Serial.print(",ACS="); Serial.print(currentRaw);
  Serial.print(",WATER="); Serial.print(waterValue);
  Serial.print(",MQ135="); Serial.print(mq135Value);
  Serial.print(",PIR1="); Serial.print(pir1);
  Serial.print(",PIR2="); Serial.print(pir2);
  Serial.print(",PARK1="); Serial.print(park1);
  Serial.print(",PARK2="); Serial.print(park2);
  Serial.print(",FLAME="); Serial.print(flame);
  Serial.print(",FIRE="); Serial.print(fireDetected ? 1 : 0);
  Serial.print(",BUZZER="); Serial.print(fireDetected ? 1 : 0);
  Serial.print(",FAN=0");
  Serial.print(",LIGHT=");
  Serial.println((pir1 == HIGH || pir2 == HIGH) ? 1 : 0);

  delay(1000);
}