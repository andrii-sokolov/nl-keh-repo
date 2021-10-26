#include <FS.h>
#include <SD.h>
#include <SPI.h>

#include <M5Stack.h>
#include "utility/MPU9250.h"
#include "utility/quaternionFilters.h"
#include "utility/M5Timer.h"

#define processing_out  true
#define AHRS true            // Set to false for basic data read
#define SerialDebug false    // Set to true to get Serial output for debugging
#define LCD

MPU9250 IMU;
// Kalman kalmanX, kalmanY, kalmanZ; // Create the Kalman instances

#define npoints 60000
/*
double b[60000];
double bufer_ax[npoints];
double bufer_ay[npoints];
double bufer_az[npoints];
*/
uint16_t i;

void writeFile(fs::FS &fs, const char * path, const char * message)
{
    M5.Lcd.printf("Writing file: %s\n", path);

    File file = fs.open(path, FILE_WRITE);
    if(!file){
        M5.Lcd.println("Failed to open file for writing");
        return;
    }
    if(file.print(message)){
        M5.Lcd.println("File written");
    } else {
        M5.Lcd.println("Write failed");
    }
}

void setup()
{
  M5.begin();
  Wire.begin();

  byte c = IMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  if (c == 0x71) // WHO_AM_I should always be 0x68
  {
    // Start by performing self test and reporting values
    IMU.MPU9250SelfTest(IMU.SelfTest);

    // Calibrate gyro and accelerometers, load biases in bias registers
    IMU.calibrateMPU9250(IMU.gyroBias, IMU.accelBias);

    IMU.initMPU9250();
  }
  else
  {
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextColor(GREEN ,BLACK);
      M5.Lcd.setCursor(0, 0); M5.Lcd.print("MPU9250 initialization Error!");
  }
  M5.Lcd.fillScreen(BLACK);

  i=0;

  //b[0] = 0.0;

}

void loop()
{
  // If intPin goes high, all data registers have new data
  // On interrupt, check if data ready interrupt
  if (IMU.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)
  {  
    IMU.readAccelData(IMU.accelCount);  // Read the x/y/z adc values
    IMU.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    IMU.ax = (float)IMU.accelCount[0]*IMU.aRes; // - accelBias[0];
    IMU.ay = (float)IMU.accelCount[1]*IMU.aRes; // - accelBias[1];
    IMU.az = (float)IMU.accelCount[2]*IMU.aRes; // - accelBias[2];

  } // if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)

    // Must be called before updating quaternions!
    IMU.updateTime();
    MahonyQuaternionUpdate(IMU.ax, IMU.ay, IMU.az, IMU.gx*DEG_TO_RAD,
                         IMU.gy*DEG_TO_RAD, IMU.gz*DEG_TO_RAD, IMU.my,
                         IMU.mx, IMU.mz, IMU.deltat);

    // Serial print and/or display at 0.5 s rate independent of data rates
    IMU.delt_t = millis() - IMU.count;

    // update LCD once per half-second independent of read rate
    // if (IMU.delt_t > 500)
    if (IMU.delt_t > 500)
    {

#ifdef LCD
      //M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextFont(2);

      M5.Lcd.setCursor(0, 0); M5.Lcd.print("     x       y       z ");
      M5.Lcd.setCursor(0,  24);
      M5.Lcd.printf("% 6d  % 6d  % 6d     mg   \r\n",  (int)(1000*IMU.ax), (int)(1000*IMU.ay), (int)(1000*IMU.az));
      M5.Lcd.setCursor(0,  44);
      M5.Lcd.printf("% 6d \r\n",IMU.delt_t);
      M5.Lcd.setCursor(20,  64);
      M5.Lcd.printf("% 6d \r\n",i);

      M5.Lcd.setCursor(12, 144); 
      M5.Lcd.print("rt: ");
      M5.Lcd.print((float) IMU.sumCount / IMU.sum, 2);
      M5.Lcd.print(" Hz");
#endif // LCD

      IMU.count = millis();
      IMU.sumCount = 0;
      IMU.sum = 0;

    } // if (IMU.delt_t > 500)

    if (i<npoints)
    {
      //b[i] = 0.0;
      i++;
    } // if (i<npoints)
    else
    {
      i=0;
    }
    
}
