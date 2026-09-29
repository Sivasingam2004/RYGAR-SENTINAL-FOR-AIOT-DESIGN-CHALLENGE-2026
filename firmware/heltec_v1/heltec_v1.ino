#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* UNO_Q_URL = "http://10.148.119.146:5000/node2";

HardwareSerial unoSerial(2);

#define UNO_RX 21
#define UNO_TX 17

#define DHT_PIN 25
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

String unoData = "";
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);

  unoSerial.begin(9600, SERIAL_8N1, UNO_RX, UNO_TX);

  dht.begin();

  delay(1000);

  Serial.println();
  Serial.println("================================");
  Serial.println(" RYGAR SENTINEL - NODE 2");
  Serial.println(" HELTEC V1");
  Serial.println("================================");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");

  Serial.print("Heltec IP: ");
  Serial.println(WiFi.localIP());

  Serial.print("UNO Q: ");
  Serial.println(UNO_Q_URL);

  Serial.println("UART READY");
}

void loop() {

  while (unoSerial.available()) {

    String data = unoSerial.readStringUntil('\n');
    data.trim();

    if (data.length() > 0) {

      if (data.startsWith("NODE2,")) {

        unoData = data;

        Serial.print("UNO: ");
        Serial.println(unoData);
      }
    }
  }

  if (millis() - lastSend >= 1000) {

    lastSend = millis();

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (WiFi.status() == WL_CONNECTED && unoData.length() > 0) {

      HTTPClient http;

      http.setTimeout(1000);
      http.begin(UNO_Q_URL);

      http.addHeader("Content-Type", "application/json");

      String json = "{";

      json += "\"node\":\"edge_02\",";

      if (!isnan(temperature)) {
        json += "\"temperature\":";
        json += String(temperature, 1);
      } else {
        json += "\"temperature\":null";
      }

      json += ",";

      if (!isnan(humidity)) {
        json += "\"humidity\":";
        json += String(humidity, 1);
      } else {
        json += "\"humidity\":null";
      }

      json += ",";

      json += "\"uno_data\":\"";
      json += unoData;
      json += "\"";

      json += "}";

      Serial.print("Sending: ");
      Serial.println(json);

      int responseCode = http.POST(json);

      Serial.print("UNO Q HTTP: ");
      Serial.println(responseCode);

      if (responseCode > 0) {

        String response = http.getString();

        Serial.print("Q Response: ");
        Serial.println(response);
      }

      http.end();

    } else {

      Serial.println("Waiting for WiFi / UNO data...");
    }
  }
}