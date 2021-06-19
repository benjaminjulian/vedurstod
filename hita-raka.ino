#include "DHT.h"

// þessi include má fjarlægja ef bara hita-raka-mælirinn er notaður:
#include <Wire.h>
#include "Adafruit_SGP30.h"
#include <SPI.h>
#include <Adafruit_BMP280.h>

#define DHTPIN A1
#define DHTTYPE DHT11

// næstu þrjár línur mega fjúka ef bara hita-raka-mælirinn er notaður:
Adafruit_SGP30 sgp;
Adafruit_BMP280 bmp; // use I2C interface
Adafruit_Sensor *bmp_pressure = bmp.getPressureSensor();

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  dht.begin();
  
  // Afgangurinn af fallinu má fara ef bara hita-raka-mælirinn er notaður:
  bmp.begin();
  sgp.begin();
  
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    return;
  }

  Serial.print("raki:");
  Serial.println(h);
  Serial.print("hiti:");
  Serial.println(t);
  
  // Allt fram að delay fallinu má fara ef bara hita-raka-mælirinn er notaður:
  
  sensors_event_t temp_event, pressure_event;
  bmp_pressure->getEvent(&pressure_event);
  
  if (! sgp.IAQmeasure()) {
    Serial.println("villa í skynjara");
    return;
  }
  Serial.print("eco2:");
  Serial.println(sgp.eCO2);
  Serial.print("hpa:");
  Serial.println(pressure_event.pressure);
  
  delay(300000);
}
