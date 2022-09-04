#include<Wire.h>
#include <SPI.h>
#include "SdFat.h"
#include "FreeStack.h"
#include "BinDataLogger.h"

// SD chip select pin.
const uint8_t SD_CS_PIN = SS;


const int MPU_addr=0x68; // I2C address of the MPU-6050
const int MPU2_addr=0x69; // I2C address of the MPU-6050

volatile bool timerFlag;
volatile uint16_t overrun;

block_t* buf;
int temp;

// SD file related function and variables
SdFat sd;
SdBaseFile binFile;

void fatalflash(){
  while(1){
    digitalWrite(2, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    delay(500);
  }
}

// max number of blocks to erase per erase call
uint32_t const ERASE_SIZE = 1024;
const uint32_t FILE_BLOCK_COUNT = 1024;

#define TMP_FILE_NAME "tmp_log.bin"
#define FILE_BASE_NAME "sensor"
// Size of file base name.  Must not be larger than six.
const uint8_t BASE_NAME_SIZE = sizeof(FILE_BASE_NAME) - 1;
char binName[13] = FILE_BASE_NAME "00.bin";

// data logging function
void logData() {
  //Serial.println(F("Creating new file"));  // use F() function to avoid using RAM for the string
  uint32_t bgnBlock, endBlock;

  // Find unused file name.
  while (sd.exists(binName)) {
    if (binName[BASE_NAME_SIZE + 1] != '9') {
      binName[BASE_NAME_SIZE + 1]++;
    } else {
      binName[BASE_NAME_SIZE + 1] = '0';
      if (binName[BASE_NAME_SIZE] == '9') {
        fatalflash();
        //Serial.println(F("Can't create file name"));
      }
      binName[BASE_NAME_SIZE]++;
    }
  }
  // Delete old tmp file.
  if (sd.exists(TMP_FILE_NAME)) {
   // Serial.println(F("Deleting tmp file"));
    if (!sd.remove(TMP_FILE_NAME)) {
      fatalflash();
      //Serial.println(F("Can't remove tmp file"));
    }
  }
  binFile.close();  
  if (!binFile.createContiguous(TMP_FILE_NAME, 512 * FILE_BLOCK_COUNT)) {
    fatalflash();
      //Serial.println(F("createContiguous failed"));
  }
  // Get the address of the file on the SD.
  if (!binFile.contiguousRange(&bgnBlock, &endBlock)) {
    fatalflash();
    //Serial.println(F("contiguousRange failed"));
  }
    
  // Use SdFat's internal buffer.
  uint8_t* cache = (uint8_t*)sd.vol()->cacheClear();
  if (cache == 0) {
    fatalflash();
    //Serial.println(F("cacheClear failed"));
  }
  // erase flash data in the allocated range
  if (!sd.card()->erase(bgnBlock, endBlock)) {
    fatalflash();
     // Serial.println(F("erase failed"));
  }
  // Start a multiple block write.
  if (!sd.card()->writeStart(bgnBlock, FILE_BLOCK_COUNT)) {
    fatalflash();
    //Serial.println(F("writeBegin failed"));
  }

  // Use SdFat buffer as buffer.
  buf = (block_t*)cache;
  
  // Give SD time to prepare for big write.
  delay(1000);
  //Serial.println(F("Logging - type any character to stop"));
  // Wait for Serial Idle.
  //Serial.flush();
  //delay(10);
  
  uint32_t bn = 0;
  //uint32_t t0 = millis();
  //uint32_t t1 = t0;
  //uint32_t overruns = 0;
  //uint32_t count = 0;
  //uint32_t maxLatency = 0; 

  // reset the buffer
  buf->count=0;

  // light the green led to indicate the start of data recording
digitalWrite(2, HIGH);
  
  // start interrupt
  timerFlag = false;
  overrun = 0;
  TIMSK1 |= (1 << OCIE1A);
  
  // read MPU data at when timerFlag is true
  while (1) {
    if (timerFlag) {
      // read MPU data
      // read IMU 1
      Wire.beginTransmission(MPU_addr);
      Wire.write(0x3B); // starting with register 0x3B(ACCEL_XOUT_H)
      Wire.endTransmission(false);
      Wire.requestFrom(MPU_addr,14,true); // request a total of14 registers
      for (int k=0; k<6; k++) {
        buf->data[buf->count++]=Wire.read();  //ACC data, MSB first
      }
      temp=Wire.read()<<8|Wire.read();   // read temperature
      for (int k=0; k<6; k++) {
        buf->data[buf->count++]=Wire.read();  //Gyro data, MSB first
      }
      Wire.endTransmission(true);

      // read IMU 2
      Wire.beginTransmission(MPU2_addr);
      Wire.write(0x3B); // starting with register 0x3B(ACCEL_XOUT_H)
      Wire.endTransmission(false);
      Wire.requestFrom(MPU2_addr,14,true); // request a total of14 registers
      for (int k=0; k<6; k++) {
        buf->data[buf->count++]=Wire.read();  //ACC data, MSB first
      }
      temp=Wire.read()<<8|Wire.read();   // read temperature
      for (int k=0; k<6; k++) {
        buf->data[buf->count++]=Wire.read();  //Gyro data, MSB first
      }
      Wire.endTransmission(true);

      // check if the buffer is full
      if (buf->count >= 504) {
        buf->timetag=micros();          // write the time tag
        buf->overrun = overrun;         // write the overrun number
        // Write block to SD.
        uint32_t usec = micros();
        if (!sd.card()->writeData((uint8_t*)buf)) {
          fatalflash();
          //Serial.println(F("write data failed"));
        }
        
        // performance monitoring operation
        //usec = micros() - usec;
        //t1 = millis();
        //if (usec > maxLatency) {
        //  maxLatency = usec;
        //}
        //count += 504;

        // reset buf and clear overrun
        buf->count = 0;
        overrun = 0;

        // monitoring is the maximum block number is reached
        bn++;
        if (bn == FILE_BLOCK_COUNT) {
          // File full so stop ISR calls.
          TIMSK1 =0;   // stop interrupts
          break;
        }
      }

      // clear timerFlag
      timerFlag = false;
    }

    // check if recording switch is off
    if (digitalRead(A1)==LOW) {
      TIMSK1 =0;    // stop interrupts
      break;
    }
  }    // end while (1)

  // stop writing
  if (!sd.card()->writeStop()) {
    fatalflash();
    //Serial.println(F("writeStop failed"));
  }
  // Truncate file if recording stopped early.
  if (bn != FILE_BLOCK_COUNT) {
    //Serial.println(F("Truncating file"));
    if (!binFile.truncate(512L * bn)) {
      fatalflash();
      //Serial.println(F("Can't truncate file"));
    }
  }
  // rename the data file
  if (!binFile.rename(binName)) {
    fatalflash();
    //Serial.println(F("Can't rename file"));
  }

  // turn the LED to indicate the end of data recording
    digitalWrite(2, LOW);
  // print message
  //Serial.print(bn);
  //Serial.println(F(" Blocks were written into file"));
  //Serial.print(F("count= "));
  //Serial.println(count);
  //Serial.print(F("Maximum writting latency: "));
  //Serial.println(maxLatency);
}

//==============================================================================
// Timer1 interrupt service routine
ISR(TIMER1_COMPA_vect){
  if (timerFlag) overrun++;

  timerFlag=true;
}

void setup() {
 // Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(A1, INPUT);
  
  // Initialize at the highest speed supported by the board that is
  // not over 50 MHz. Try a lower speed if SPI errors occur.
  if (!sd.begin(SD_CS_PIN, SD_SCK_MHZ(50))) {
    sd.initErrorPrint();
    fatalflash();
    //Serial.println(F("Setting SPI Failed"));
  }

  // setup I2C communication to IMU and write IMU register
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  
  Wire.begin();
  Wire.beginTransmission(MPU2_addr);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // setup timer 1
  //Serial.println(F("Setup timer 1"));
  delay(100);
  cli();
  //set timer1 interrupt at 125Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 125Hz sampling rate
  OCR1A = 1999;// = (16*10^6) / (125*64 - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS11 bits for 64 prescaler
  TCCR1B |= (1 << CS11) | (1 << CS10);  
  // enable timer compare interrupt
  //TIMSK1 |= (1 << OCIE1A); 
  sei();//allow interrupts
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println(F("Type any key to start data logging"));
  //while(!Serial.available()) {
    //SysCall::yield();
  //}
  
  // Read any Serial data.
  //do {
    //delay(10);
  //} while (Serial.available() && Serial.read() >= 0);

  //Serial.flush();
  delay(100);
   if (digitalRead(A1)==HIGH){
    logData();}
}
