#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* UNO_Q_URL = "http://10.148.119.146:5000/entrance";

HardwareSerial unoSerial(2);

#define RX2_PIN 16
#define TX2_PIN 17

void setup() {
  Serial.begin(115200);

  unoSerial.begin(9600, SERIAL_8N1, RX2_PIN, TX2_PIN);

  delay(1000);

  Serial.println("RYGAR SENTINEL - ENTRANCE NODE");
  Serial.println("UART READY");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");

  Serial.print("Entrance ESP32 IP: ");
  Serial.println(WiFi.localIP());

  Serial.print("UNO Q: ");
  Serial.println(UNO_Q_URL);
}

void loop() {

  if (unoSerial.available() > 0) {

    String event = unoSerial.readStringUntil('\n');
    event.trim();

    if (event.length() == 0) {
      return;
    }

    Serial.print("UNO EVENT: [");
    Serial.print(event);
    Serial.println("]");

    if (WiFi.status() == WL_CONNECTED) {

      HTTPClient http;

      http.setTimeout(2000);

      http.begin(UNO_Q_URL);

      http.addHeader("Content-Type", "application/json");

      String json = "{\"node\":\"entrance\",\"event\":\"";
      json += event;
      json += "\"}";

      int responseCode = http.POST(json);

      Serial.print("UNO Q HTTP: ");
      Serial.println(responseCode);

      if (responseCode > 0) {

        String response = http.getString();

        Serial.print("Q Response: ");
        Serial.println(response);
      }

      http.end();
    }
  }
}