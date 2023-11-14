import os
import serial
import time
import datetime
import sys
import numpy as np

class SDS011Reader:
    """This is a wrapper for the implimentation from ronanj"""

    def __init__(self, inport = "/dev/ttyUSB0"):
        self.serial = serial.Serial(port=inport,baudrate=9600)
    
    def close(self):
        self.serial.close()

    def sensor_wake(self):
        self.serial.write(b'\x01')
    
    def sensor_sleep(self):
        bytes = ['\xaa', #head
        '\xb4', #command 1
        '\x06', #data byte 1
        '\x01', #data byte 2 (set mode)
        '\x00', #data byte 3 (sleep)
        '\x00', #data byte 4
        '\x00', #data byte 5
        '\x00', #data byte 6
        '\x00', #data byte 7
        '\x00', #data byte 8
        '\x00', #data byte 9
        '\x00', #data byte 10
        '\x00', #data byte 11
        '\x00', #data byte 12
        '\x00', #data byte 13
        '\xff', #data byte 14 (device id byte 1)
        '\xff', #data byte 15 (device id byte 2)
        '\x05', #checksum+","+
        '\xab'] #tail
        for b in bytes:
            self.serial.write(b)
    
    def readValue(self):
        self.sensor_wake()
        # time.sleep(15)
        step = 0
        while True: 
            while self.serial.inWaiting()!=0:
                v=ord(self.serial.read())

                if step ==0:
                    if v==170:
                        step=1

                elif step==1:
                    if v==192:
                        values = [0,0,0,0,0,0,0]
                        step=2
                    else:
                        step=0

                elif step>8:
                    step =0
                    pm25 = float(values[0]+values[1]*256)/10 #divided by 10 to get correct values
                    pm10 = float(values[2]+values[3]*256)/10
                    
                    return [pm25,pm10]

                elif step>=2:
                    values[step-2]=v
                    step= step+1
        # time.sleep(5)
        self.sensor_sleep()
        # time.sleep(3)
        self.close()
