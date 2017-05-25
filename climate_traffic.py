# -*- coding: utf-8 -*-
"""
Created on Sun May 21 20:46:26 2017

@author: pi
"""

# Import relevant libraries
from sense_hat import SenseHat
sense = SenseHat()

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

import pandas as pd
import numpy as np

# Create dataframe for readings
readings = pd.DataFrame()

# Clear LED panel, set to low light
sense.clear()
sense.low_light = True


# Take readings every 60 seconds
@sched.scheduled_job('interval', seconds=60)
def take_readings():
    ## MEASUREMENT ##    
    # Take readings
    timestamp = str(datetime.now())
    humidity = sense.get_humidity()
    temp = sense.get_temperature()
    pressure = sense.get_pressure()

    # Print readings to terminal
    print(timestamp)
    print("Temperature:\t %s C" % round(temp, 1))
    print("Humidity:\t %s %%rH" % round(humidity, 1))
    print("Pressure:\t %s Millibars\n" % round(pressure, 1))

    # Add readings to dataframe.
    global readings    
    readings = readings.append({'timestamp': timestamp, 'T': temp, 'H': humidity, 'P': pressure }, 
                           ignore_index=True)
    
    ## ANALYSIS ##
    # Separate out datasets for the last 10, 20 and 30 minutes
    readingsA = readings.tail(10)
    readingsB = readings.tail(20)
    readingsC = readings.tail(30)    
    
    # Work out mean values for each time frame
    TmeanA = readingsA["T"].mean()
    TmeanB = readingsB["T"].mean()
    TmeanC = readingsC["T"].mean()
    HmeanA = readingsA["H"].mean()
    HmeanB = readingsB["H"].mean()
    HmeanC = readingsC["H"].mean()
    PmeanA = readingsA["P"].mean()
    PmeanB = readingsB["P"].mean()
    PmeanC = readingsC["P"].mean()
    
    # Work out standard deviations for each time frame
    TdevA = readingsA["T"].std()
    TdevB = readingsB["T"].std()
    TdevC = readingsC["T"].std()
    HdevA = readingsA["H"].std()
    HdevB = readingsB["H"].std()
    HdevC = readingsC["H"].std()
    PdevA = readingsA["P"].std()
    PdevB = readingsB["P"].std()
    PdevC = readingsC["P"].std()

    # Print table with metrics
    print("10 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(TmeanA, 1), round(TdevA, 2)))
    print("Humidity\t %s\t %s" % (round(HmeanA, 1), round(HdevA, 2)))
    print("Pressure\t %s\t %s\n" % (round(PmeanA, 1), round(PdevA, 2)))

    print("20 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(TmeanB, 1), round(TdevB, 2)))
    print("Humidity\t %s\t %s" % (round(HmeanB, 1), round(HdevB, 2)))
    print("Pressure\t %s\t %s\n" % (round(PmeanB, 1), round(PdevB, 2)))
    
    print("30 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(TmeanC, 1), round(TdevC, 2)))
    print("Humidity\t %s\t %s" % (round(HmeanC, 1), round(HdevC, 2)))
    print("Pressure\t %s\t %s\n" % (round(PmeanC, 1), round(PdevC, 2)))

    # 10 min temp test
    #print("Over the past 10 minutes, temperature is within:")
    if temp <= TmeanA - 2*TdevA:
        #print("-2sd\n")
        sense.set_pixel(0, 0, 255, 0, 0)
    elif temp <= TmeanA - TdevA:
        #print("-1sd\n")
        sense.set_pixel(0, 0, 255, 255, 0)
    elif temp >= TmeanA + 2*TdevA:
        #print("+2sd\n")
        sense.set_pixel(0, 0, 255, 0, 0)
    elif temp >= TmeanA + TdevA:
        #print("+1sd\n")
        sense.set_pixel(0, 0, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(0, 0, 0, 255, 0)

    # 20 min temp test
    #print("Over the past 20 minutes, temperature is within:")
    if temp <= TmeanB - 2*TdevB:
        #print("-2sd\n")
        sense.set_pixel(1, 0, 255, 0, 0)
    elif temp <= TmeanB - TdevB:
        #print("-1sd\n")
        sense.set_pixel(1, 0, 255, 255, 0)
    elif temp >= TmeanB + 2*TdevB:
        #print("+2sd\n")
        sense.set_pixel(1, 0, 255, 0, 0)
    elif temp >= TmeanB + TdevB:
        #print("+1sd\n")
        sense.set_pixel(1, 0, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(1, 0, 0, 255, 0)

    # 30 min temp test
    #print("Over the past 30 minutes, temperature is within:")
    if temp <= TmeanC - 2*TdevC:
        #print("-2sd\n")
        sense.set_pixel(2, 0, 255, 0, 0)
    elif temp <= TmeanC - TdevC:
        #print("-1sd\n")
        sense.set_pixel(2, 0, 255, 255, 0)
    elif temp >= TmeanC + 2*TdevC:
        #print("+2sd\n")
        sense.set_pixel(2, 0, 255, 0, 0)
    elif temp >= TmeanC + TdevC:
        #print("+1sd\n")
        sense.set_pixel(2, 0, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(2, 0, 0, 255, 0)

    # 10 min humidity test
    #print("Over the past 10 minutes, humidity is within:")
    if humidity <= HmeanA - 2*HdevA:
        #print("-2sd\n")
        sense.set_pixel(0, 1, 255, 0, 0)
    elif humidity <= HmeanA - HdevA:
        #print("-1sd\n")
        sense.set_pixel(0, 1, 255, 255, 0)
    elif humidity >= HmeanA + 2*HdevA:
        #print("+2sd\n")
        sense.set_pixel(0, 1, 255, 0, 0)
    elif humidity >= HmeanA + HdevA:
        #print("+1sd\n")
        sense.set_pixel(0, 1, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(0, 1, 0, 255, 0)

    # 20 min humidity test
    #print("Over the past 20 minutes, humidity is within:")
    if humidity <= HmeanB - 2*HdevB:
        #print("-2sd\n")
        sense.set_pixel(1, 1, 255, 0, 0)
    elif humidity <= HmeanB - HdevB:
        #print("-1sd\n")
        sense.set_pixel(1, 1, 255, 255, 0)
    elif humidity >= HmeanB + 2*HdevB:
        #print("+2sd\n")
        sense.set_pixel(1, 1, 255, 0, 0)
    elif humidity >= HmeanB + HdevB:
        #print("+1sd\n")
        sense.set_pixel(1, 1, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(1, 1, 0, 255, 0)

    # 30 min humidity test
    #print("Over the past 30 minutes, humidity is within:")
    if humidity <= HmeanC - 2*HdevC:
        #print("-2sd\n")
        sense.set_pixel(2, 1, 255, 0, 0)
    elif humidity <= HmeanC - HdevC:
        #print("-1sd\n")
        sense.set_pixel(2, 1, 255, 255, 0)
    elif humidity >= HmeanC + 2*HdevC:
        #print("+2sd\n")
        sense.set_pixel(2, 1, 255, 0, 0)
    elif humidity >= HmeanC + HdevC:
        #print("+1sd\n")
        sense.set_pixel(2, 1, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(2, 1, 0, 255, 0)

    # 10 min pressure test
    #print("Over the past 10 minutes, pressure is within:")
    if pressure <= PmeanA - 2*PdevA:
        #print("-2sd\n")
        sense.set_pixel(0, 2, 255, 0, 0)
    elif pressure <= PmeanA - PdevA:
        #print("-1sd\n")
        sense.set_pixel(0, 2, 255, 255, 0)
    elif pressure >= PmeanA + 2*PdevA:
        #print("+2sd\n")
        sense.set_pixel(0, 2, 255, 0, 0)
    elif pressure >= PmeanA + PdevA:
        #print("+1sd\n")
        sense.set_pixel(0, 2, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(0, 2, 0, 255, 0)

    # 20 min pressure test
    #print("Over the past 20 minutes, pressure is within:")
    if pressure <= PmeanB - 2*PdevB:
        #print("-2sd\n")
        sense.set_pixel(1, 2, 255, 0, 0)
    elif pressure <= PmeanB - PdevB:
        #print("-1sd\n")
        sense.set_pixel(1, 2, 255, 255, 0)
    elif pressure >= PmeanB + 2*PdevB:
        #print("+2sd\n")
        sense.set_pixel(1, 2, 255, 0, 0)
    elif pressure >= PmeanB + PdevB:
        #print("+1sd\n")
        sense.set_pixel(1, 2, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(1, 2, 0, 255, 0)

    # 30 min pressure test
    #print("Over the past 30 minutes, pressure is within:")
    if pressure <= PmeanC - 2*PdevC:
        #print("-2sd\n")
        sense.set_pixel(2, 2, 255, 0, 0)
    elif pressure <= PmeanC - PdevC:
        #print("-1sd\n")
        sense.set_pixel(2, 2, 255, 255, 0)
    elif pressure >= PmeanC + 2*PdevC:
        #print("+2sd\n")
        sense.set_pixel(2, 2, 255, 0, 0)
    elif pressure >= PmeanC + PdevC:
        #print("+1sd\n")
        sense.set_pixel(2, 2, 255, 255, 0)
    else:
        #print("mean\n")
        sense.set_pixel(2, 2, 0, 255, 0)

@sched.scheduled_job('interval', seconds=3600)
def store_readings():
    timestamp = str(datetime.now())    
    readings.to_csv('/home/pi/Desktop/climatestation/reading\ %s.csv' % timestamp)

sched.start()