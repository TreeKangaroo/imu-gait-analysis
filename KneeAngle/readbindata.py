# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 22:09:19 2019

@author: study
"""
import numpy as np

def readbinFile(filename):
    byte_num = 504
    interval = 168000
    tol = 20

    blk_num = 0
    last_timetag = 0
    err_flag=False

    with open(filename, "rb") as f:
        while True:
            block=f.read(512)
            if not block:
                break
            else:
                blk_num=blk_num+1
                count=int.from_bytes(block[0:2], byteorder="little", signed=False)
                if count != byte_num:
                    print("Incorrect number of bytes in Block: ", blk_num);
                    err_flag=True
                    
                overrun=int.from_bytes(block[2:4], byteorder="little", signed=False)
                if overrun:
                    print("Overrun error at Block: ", blk_num, overrun)
                    err_flag=True
                    
                timetag=int.from_bytes(block[4:8], byteorder="little", signed=False)
                if blk_num>=2:
                    time_diff = timetag-last_timetag
                    if time_diff>(interval+tol) or time_diff<(interval-tol):
                        print("Timetage error in Block: ", blk_num, time_diff)
                        err_flag=True
                        
                last_timetag = timetag
            
    # remove the last block
    num=blk_num*21
    data = np.zeros((num, 12))
    n=0

    with open(filename, "rb") as f:
        while True:
            block=f.read(512)
            if not block:
                break
            else:
                for k in range(21):
                    m=8+k*24
                    for j in range(12):
                        p=m+j*2
                        data[n, j]=int.from_bytes(block[p:p+2], byteorder="big", signed=True)
                    n=n+1
    
    return err_flag, data
    

err_flag, sensordata = readbinFile("sensor00.bin")  

np.savetxt("sensor00.txt", data, fmt='%5d', delimiter=' ')         