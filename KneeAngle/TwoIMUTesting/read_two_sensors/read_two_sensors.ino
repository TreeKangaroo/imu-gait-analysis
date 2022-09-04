// MPU-6050 Short Example Sketch
// By Arduino User JohnChi
// August 17, 2014
// Public Domain
#include<Wire.h>
const int MPU1_addr=0x68; // I2C address of the MPU-6050
const int MPU2_addr=0x69;
int16_t AcX1,AcY1,AcZ1,Tmp1,GyX1,GyY1,GyZ1,count,AcX2,AcY2,AcZ2,Tmp2,GyX2,GyY2,GyZ2;

uint32_t pt, ct, period;


void setup(){
Wire.begin();
Wire.beginTransmission(MPU1_addr);
Wire.write(0x6B); // PWR_MGMT_1 register
Wire.write(0); // set to zero (wakes up the MPU-6050)
Wire.endTransmission(true);

Serial.begin(1000000);

Wire.begin();
Wire.beginTransmission(MPU2_addr);
Wire.write(0x6B); // PWR_MGMT_1 register
Wire.write(0); // set to zero (wakes up the MPU-6050)
Wire.endTransmission(true);

period=8000;      // read sensor every 4ms, about 250Hz sampling rate
count=0;
delay(1000);
pt=micros();
Serial.println("#start test, sesnor configure register data are:");

  Wire.beginTransmission(MPU1_addr);
  Wire.write(0x19);       // move register pointer to SMPLRT_div reg
  Wire.endTransmission(false);
  Wire.requestFrom(MPU1_addr, 4, true); // request 4 register
  uint8_t srdivreg = Wire.read();
  uint8_t confreg = Wire.read();
  uint8_t gyroreg = Wire.read();
  uint8_t accreg = Wire.read();
  Wire.endTransmission(true);
  Serial.print("#Sampling rate divider1: ");
  Serial.println(srdivreg);
  Serial.print("#Config register1: ");
  Serial.println(confreg);
  Serial.print("#Gyrometer config register1: ");
  Serial.println(gyroreg);
  Serial.print("#Acceleromter config register1: ");
  Serial.println(accreg);

  Wire.beginTransmission(MPU2_addr);
  Wire.write(0x19);       // move register pointer to SMPLRT_div reg
  Wire.endTransmission(false);
  Wire.requestFrom(MPU2_addr, 4, true); // request 4 register
  srdivreg = Wire.read();
  confreg = Wire.read();
  gyroreg = Wire.read();
  accreg = Wire.read();
  Wire.endTransmission(true);
  Serial.print("#Sampling rate divider2: ");
  Serial.println(srdivreg);
  Serial.print("#Config register2: ");
  Serial.println(confreg);
  Serial.print("#Gyrometer config register2: ");
  Serial.println(gyroreg);
  Serial.print("#Acceleromter config register2: ");
  Serial.println(accreg);

}
void loop(){
  while(1){
  ct=micros();
  if(ct-pt>period){
    pt=ct;
    Wire.beginTransmission(MPU1_addr);
    Wire.write(0x3B); // starting with register 0x3B(ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU1_addr,14,true); // request a total of14 registers
    AcX1=Wire.read()<<8|Wire.read(); // 0x3B (ACCEL_XOUT_H) &0x3C (ACCEL_XOUT_L)
    AcY1=Wire.read()<<8|Wire.read(); // 0x3D (ACCEL_YOUT_H) &0x3E (ACCEL_YOUT_L)
    AcZ1=Wire.read()<<8|Wire.read(); // 0x3F (ACCEL_ZOUT_H) &0x40 (ACCEL_ZOUT_L)
    Tmp1=Wire.read()<<8|Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42(TEMP_OUT_L)
    GyX1=Wire.read()<<8|Wire.read(); // 0x43 (GYRO_XOUT_H) &0x44 (GYRO_XOUT_L)
    GyY1=Wire.read()<<8|Wire.read(); // 0x45 (GYRO_YOUT_H) &0x46 (GYRO_YOUT_L)
    GyZ1=Wire.read()<<8|Wire.read(); // 0x47 (GYRO_ZOUT_H) &0x48 (GYRO_ZOUT_L)
    Wire.endTransmission(true);

    Wire.beginTransmission(MPU2_addr);
    Wire.write(0x3B); // starting with register 0x3B(ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU2_addr,14,true); // request a total of14 registers
    AcX2=Wire.read()<<8|Wire.read(); // 0x3B (ACCEL_XOUT_H) &0x3C (ACCEL_XOUT_L)
    AcY2=Wire.read()<<8|Wire.read(); // 0x3D (ACCEL_YOUT_H) &0x3E (ACCEL_YOUT_L)
    AcZ2=Wire.read()<<8|Wire.read(); // 0x3F (ACCEL_ZOUT_H) &0x40 (ACCEL_ZOUT_L)
    Tmp2=Wire.read()<<8|Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42(TEMP_OUT_L)
    GyX2=Wire.read()<<8|Wire.read(); // 0x43 (GYRO_XOUT_H) &0x44 (GYRO_XOUT_L)
    GyY2=Wire.read()<<8|Wire.read(); // 0x45 (GYRO_YOUT_H) &0x46 (GYRO_YOUT_L)
    GyZ2=Wire.read()<<8|Wire.read(); // 0x47 (GYRO_ZOUT_H) &0x48 (GYRO_ZOUT_L)
    Wire.endTransmission(true);
    
    // print sensor data
    Serial.print(AcX1);
    Serial.print(" ");
    Serial.print(AcY1);
    Serial.print(" ");
    Serial.print(AcZ1);
    Serial.print(" ");
    Serial.print(GyX1);
    Serial.print(" ");
    Serial.print(GyY1);
    Serial.print(" ");
    Serial.print(GyZ1);
    Serial.print(" ");

    Serial.print(AcX2);
    Serial.print(" ");
    Serial.print(AcY2);
    Serial.print(" ");
    Serial.print(AcZ2);
    Serial.print(" ");
    Serial.print(GyX2);
    Serial.print(" ");
    Serial.print(GyY2);
    Serial.print(" ");
    Serial.print(GyZ2);
    Serial.print(" ");
    Serial.println(ct);
    count=count+1;
  }}
  while (1);
}
