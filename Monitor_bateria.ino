#include <WiFi.h>
#include <HTTPClient.h>

/*
 * ESP32 - VE.Direct + ThingsBoard Cloud
 * 
 * Conexiones BMV-712:
 * VE.Direct Pin 1 (GND) → ESP32 GND
 * VE.Direct Pin 2 (RX)  → ESP32 GPIO17 (TX2)
 * VE.Direct Pin 3 (TX)  → ESP32 GPIO16 (RX2)
 * VE.Direct Pin 4 (VCC) → NO CONECTAR
 */

// 🔹 Configura tu red WiFi
const char* ssid     = "KingoTaller";
const char* password = "kingotaller";

// 🔹 Configura ThingsBoard Cloud
String serverName = "http://thingsboard.cloud/api/v1/1h0kfauv3h1wrivxhjc4/telemetry";

// Variables para datos del BMV
float voltage = 0.0;
float current = 0.0;
int power = 0;
float soc = 0.0;
float energy = 0.0;

void setup() {
  Serial.begin(115200);
  delay(2000);

  // Iniciar UART2 (para VE.Direct)
  Serial2.begin(19200, SERIAL_8N1, 16, 17);

  // Conectar al WiFi
  Serial.println("\nConectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("IP ESP32: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (Serial2.available()) {
    String line = Serial2.readStringUntil('\n');
    line.trim();

    if (line.startsWith("V\t")) {
      voltage = line.substring(2).toFloat() / 1000.0;
    }
    else if (line.startsWith("I\t")) {
      current = line.substring(2).toFloat() / 1000.0;
    }
    else if (line.startsWith("P\t")) {
      power = line.substring(2).toInt();
    }
    else if (line.startsWith("SOC\t")) {
      soc = line.substring(4).toFloat() / 10.0;
    }
    else if (line.startsWith("CE\t")) {
      energy = line.substring(3).toFloat() / 1000.0;

      // ✅ Cuando recibimos CE (último valor de interés), enviamos todo a ThingsBoard Cloud
      enviarDatos();
    }
  }
  delay(10);
}

void enviarDatos() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Armar JSON con todos los valores
    String jsonData = "{";
    jsonData += "\"voltaje\":" + String(voltage, 3) + ",";
    jsonData += "\"corriente\":" + String(current, 3) + ",";
    jsonData += "\"potencia\":" + String(power) + ",";
    jsonData += "\"soc\":" + String(soc, 1) + ",";
    jsonData += "\"energia\":" + String(energy, 3);
    jsonData += "}";

    Serial.println("Enviando a ThingsBoard Cloud...");
    Serial.println(jsonData);

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("Respuesta HTTP: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Servidor: " + response);
    } else {
      Serial.print("Error al enviar: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi desconectado, no se pudo enviar.");
  }
}

