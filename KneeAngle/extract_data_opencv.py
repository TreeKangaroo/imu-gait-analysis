# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:06:14 2019

@author: study
"""

import cv2
import numpy as np
from pathlib import Path 

baseName="sensor20"
baseName1="DSC_0020"

videopath="C:\\Users\\study\\Videos\\videos4sf\\release2vids\\Weidata\\wei2"
videofile=videopath + "\\" + baseName1 + ".mov"

datapath ="C:\\Users\\study\\Dropbox\\SciFair\\Release2\\opencvData\\weidata\\wei2"
datafile=datapath + "\\" + baseName + "_opencv.txt"

# define range of green color in HSV
# change it according to your need !
sensitivity = 15
#lower_green = np.array([60-sensitivity, 100, 20])
#upper_green = np.array([60+sensitivity,255, 255])

lower_green = np.array([30, 0, 0])
upper_green = np.array([80, 255, 255])

# threshold for recognizing as a contour for filtering out small dots
minArea =2600

# frame to be saved for inspection
sel_frame = 12

# frame index
a =0

# read video file
cap = cv2.VideoCapture(videofile)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# open a text file for writing result
f = open(datafile, "w")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Threshold the HSV image to get only green colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
#    mask = cv2.erode(mask, None, iterations=1)
#    mask = cv2.dilate(mask, None, iterations=1)
    # get the contours from mask
    _, cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    a = a+1
    b = 0
    cx=0
    cy=0
    positions = []
    
    # get contour center position
    for c in cnts:
        if (cv2.contourArea(c)>minArea):        
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"]);
            cy = int(M["m01"] / M["m00"]);
            
            # check if it is splitted tracking point
            for p in positions:
                if abs(p[1]-cy)<50:
                    cx=int(0.5*(cx+p[0]))
                    cy=int(0.5*(cy+p[1]))
                    positions.remove(p)
                    b=b-1
            
            positions.append((cx, cy))       
            #print("Frame ", a, "(", cx, ",",  cy, ")" )
            # add red circles to the identified contours
            cv2.circle(frame,(cx,cy), 10, (0,0,255), -1)
            b = b+1

    # send warning message if less or more than 2 contours are found
    # otherwise, write the contour coordicates to data file
    if b<3:
        print("lose tracking in Frame:", a)
    elif b>3:
        print("false tracking points in Frame:", a)
    else:
        positions.sort(key=lambda tup: tup[1])
        pos=str(a) + " "
        for p in positions:
            pos = pos + str(p[0]) + " " + str(p[1]) + " "
        pos = pos + "\n"
        f.write(pos)
        
    # Display the resulting frame
    cv2.imshow('Frame',frame)
    
    # save the mark and annotated frame to file 
    if (a==12):
        cv2.imwrite("mask.jpg", mask)
        cv2.imwrite("frame.jpg", frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
f.close()
 
# Closes all the frames
cv2.destroyAllWindows()