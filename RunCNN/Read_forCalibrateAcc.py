# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:35:14 2019

The code shows that arduino maximum baud rate is 2,000,000 
(2M bits per second.) To transfer 14 bytes data. It takes about 
14*8/2=56 us.  
@author: study
"""

import serial
from time import sleep
import time
import numpy as np

ser = serial.Serial('COM6', 500000)

# the following code is to reset arduino
ser.setDTR(False) # Drop DTR
sleep(0.022)    # Read somewhere that 22ms is what the UI does.
ser.setDTR(True)  # UP the DTR back

acc=[]
cnt=0

ser.flushInput()
newline = ser.readline()         # read a new line
l = newline.decode()
print(l)

while cnt<100:
    ch=input("key: ")
    ser.write('a'.encode())

    for k in range(10):
        newline = ser.readline()         # read a new line
        l = newline.decode()
        s = l.rstrip()                  # remove \n and \r
        data = s.split()
        if len(data)!=3:
            print(s)
        else:
            acc.append(data[0:3])

    cnt+=1
    print(cnt)

# complete data collection save it into a text file
ser.close()
data = np.array(acc, dtype='int')
np.savetxt('cal_acc2.txt', data, delimiter=',')







