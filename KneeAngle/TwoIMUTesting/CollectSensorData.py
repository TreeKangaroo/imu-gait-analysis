# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:35:14 2019

The code shows that arduino maximum baud rate is 2,000,000 
(2M bits per second.) To transfer 14 bytes data. It takes about 
14*8/2=56 us.  
@author: study
"""

import serial
from time   import sleep

data_file = open("boardtest1.txt", "w")

ser = serial.Serial('COM5', 1000000)
ser.flushInput()
# the following code is to reset arduino
ser.setDTR(False) # Drop DTR
sleep(0.052)    # Read somewhere that 22ms is what the UI does.
ser.setDTR(True)  # UP the DTR back

numpts =2500     # number of data points to be collected
num = numpts + 5  # add 5 additional line for file header

for k in range(num):
    newline = ser.readline()         # read a new line
    l = newline.decode()
    s = l.rstrip()                  # remove \n and \r
    data_file.write(s+"\n")
    if (k==0):
        print(s)

data_file.close()
ser.close()

