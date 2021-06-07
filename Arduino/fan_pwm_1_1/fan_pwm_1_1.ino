
 /* 
  #include <Adafruit_BusIO_Register.h>
  #include <Adafruit_I2CDevice.h>
  #include <Adafruit_I2CRegister.h>
  #include <Adafruit_SPIDevice.h>
  #include <SPI.h>
  #define OLED_RESET 4
  #define SSD1306_128_32  
  display.display();  
  display.begin(SSD1306_SWITCHAPVCC, 03c);  
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.detTextSize(2);
  display.setcursor(10, 30);
  display.println(RPM)
  */
  
int sensorPin = A0;
int PWM = 3;
int sensorVal;
int PWMVal;
int count = 0;
int RPM;
unsigned long start_time;

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(PWM, OUTPUT);
  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(2),counter, RISING);
  
  

}

void loop() {
  start_time = millis();
  count = 0;
  while((millis() - start_time)< 1000){
     }RPM = count * 60/2;
  
  Serial.print(RPM);
  Serial.print(",");
  Serial.print(map(sensorVal, 620, 400, 19, 60));
  Serial.print(",");
  Serial.println(map(PWMVal,0, 255, 0, 100 ));
  delay(1000);


  sensorVal = analogRead(sensorPin);
  if(sensorVal >620){
    sensorVal = 620;
    PWMVal = 0;
  }

  PWMVal = map(sensorVal, 620, 400, 0, 255);

  if(sensorVal <400){
    PWMVal = 255;
  }
  
  analogWrite(PWM, PWMVal);

}

void counter() {
count++;
}
