#include <Keypad.h>
#include <Servo.h>

const int SERVO_PIN  = 6;
const int DOOR_PIN   = 11;
const int BUZZER_PIN = 12;

Servo doorServo;

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {7, 8, 9, 10};

Keypad keypad = Keypad(
  makeKeymap(keys),
  rowPins,
  colPins,
  ROWS,
  COLS
);

String correctPIN = "1111";
String enteredPIN = "";

bool doorWasOpen = false;

void sendEvent(const char* event) {
  Serial.println(event);
}

void setup() {
  pinMode(DOOR_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  doorServo.attach(SERVO_PIN);
  doorServo.write(0);

  Serial.begin(9600);

  delay(500);
  sendEvent("ENTRANCE_ONLINE");
}

void loop() {
  char key = keypad.getKey();

  if (key) {
    if (key == '*') {
      enteredPIN = "";
      tone(BUZZER_PIN, 1000, 100);
      return;
    }

    if (key == '#') {
      if (enteredPIN == correctPIN) {
        sendEvent("ACCESS_GRANTED");
        tone(BUZZER_PIN, 2000, 200);
        doorServo.write(90);
        delay(3000);
        doorServo.write(0);
      } else {
        sendEvent("ACCESS_DENIED");
        tone(BUZZER_PIN, 500, 800);
      }

      enteredPIN = "";
    } else {
      if (enteredPIN.length() < 8) {
        enteredPIN += key;
        tone(BUZZER_PIN, 1200, 60);
      }
    }
  }

  bool doorOpen = digitalRead(DOOR_PIN) == HIGH;

  if (doorOpen != doorWasOpen) {
    if (doorOpen) {
      sendEvent("DOOR_OPEN");
    } else {
      sendEvent("DOOR_CLOSED");
    }

    doorWasOpen = doorOpen;
  }

  delay(20);
}