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

# Clear LED panel
sense.clear()


# Take readings every 60 seconds
@sched.scheduled_job('interval', seconds=60)
def timed_job():
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
    readings10 = readings.tail(10)
    readings20 = readings.tail(20)
    readings30 = readings.tail(30)    
    
    # Work out mean values for each time frame
    Tmean10 = readings10["T"].mean()
    Tmean20 = readings20["T"].mean()
    Tmean30 = readings30["T"].mean()
    Hmean10 = readings10["H"].mean()
    Hmean20 = readings20["H"].mean()
    Hmean30 = readings30["H"].mean()
    Pmean10 = readings10["P"].mean()
    Pmean20 = readings20["P"].mean()
    Pmean30 = readings30["P"].mean()
    
    # Work out standard deviations for each time frame
    Tdev10 = readings10["T"].std()
    Tdev20 = readings20["T"].std()
    Tdev30 = readings30["T"].std()
    Hdev10 = readings10["H"].std()
    Hdev20 = readings20["H"].std()
    Hdev30 = readings30["H"].std()
    Pdev10 = readings10["P"].std()
    Pdev20 = readings20["P"].std()
    Pdev30 = readings30["P"].std()

    # Print table with metrics
    print("10 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(Tmean10, 1), round(Tdev10, 2)))
    print("Humidity\t %s\t %s" % (round(Hmean10, 1), round(Hdev10, 2)))
    print("Pressure\t %s\t %s\n" % (round(Pmean10, 1), round(Pdev10, 2)))

    print("20 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(Tmean20, 1), round(Tdev20, 2)))
    print("Humidity\t %s\t %s" % (round(Hmean20, 1), round(Hdev20, 2)))
    print("Pressure\t %s\t %s\n" % (round(Pmean20, 1), round(Pdev20, 2)))
    
    print("30 minutes\t Mean\t StdDev")
    print("Temperature\t %s\t %s" % (round(Tmean30, 1), round(Tdev30, 2)))
    print("Humidity\t %s\t %s" % (round(Hmean30, 1), round(Hdev30, 2)))
    print("Pressure\t %s\t %s\n" % (round(Pmean30, 1), round(Pdev30, 2)))

    # 10 min temp test
    print("Over the past 10 minutes, temperature is within:")
    if temp <= Tmean10 - 2*Tdev10:
        print("-2sd\n")
        sense.set_pixel(0, 0, 255, 0, 0)
    elif temp <= Tmean10 - Tdev10:
        print("-1sd\n")
        sense.set_pixel(0, 0, 255, 255, 0)
    elif temp >= Tmean10 + 2*Tdev10:
        print("+2sd\n")
        sense.set_pixel(0, 0, 255, 0, 0)
    elif temp >= Tmean10 + Tdev10:
        print("+1sd\n")
        sense.set_pixel(0, 0, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(0, 0, 0, 255, 0)

    # 20 min temp test
    print("Over the past 20 minutes, temperature is within:")
    if temp <= Tmean20 - 2*Tdev20:
        print("-2sd\n")
        sense.set_pixel(1, 0, 255, 0, 0)
    elif temp <= Tmean20 - Tdev20:
        print("-1sd\n")
        sense.set_pixel(1, 0, 255, 255, 0)
    elif temp >= Tmean20 + 2*Tdev20:
        print("+2sd\n")
        sense.set_pixel(1, 0, 255, 0, 0)
    elif temp >= Tmean20 + Tdev20:
        print("+1sd\n")
        sense.set_pixel(1, 0, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(1, 0, 0, 255, 0)

    # 30 min temp test
    print("Over the past 30 minutes, temperature is within:")
    if temp <= Tmean30 - 2*Tdev30:
        print("-2sd\n")
        sense.set_pixel(2, 0, 255, 0, 0)
    elif temp <= Tmean30 - Tdev30:
        print("-1sd\n")
        sense.set_pixel(2, 0, 255, 255, 0)
    elif temp >= Tmean30 + 2*Tdev30:
        print("+2sd\n")
        sense.set_pixel(2, 0, 255, 0, 0)
    elif temp >= Tmean30 + Tdev30:
        print("+1sd\n")
        sense.set_pixel(2, 0, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(2, 0, 0, 255, 0)

    # 10 min humidity test
    print("Over the past 10 minutes, humidity is within:")
    if humidity <= Hmean10 - 2*Hdev10:
        print("-2sd\n")
        sense.set_pixel(0, 1, 255, 0, 0)
    elif humidity <= Hmean10 - Hdev10:
        print("-1sd\n")
        sense.set_pixel(0, 1, 255, 255, 0)
    elif humidity >= Hmean10 + 2*Hdev10:
        print("+2sd\n")
        sense.set_pixel(0, 1, 255, 0, 0)
    elif humidity >= Hmean10 + Hdev10:
        print("+1sd\n")
        sense.set_pixel(0, 1, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(0, 1, 0, 255, 0)

    # 20 min humidity test
    print("Over the past 20 minutes, humidity is within:")
    if humidity <= Hmean20 - 2*Hdev20:
        print("-2sd\n")
        sense.set_pixel(1, 1, 255, 0, 0)
    elif humidity <= Hmean20 - Hdev20:
        print("-1sd\n")
        sense.set_pixel(1, 1, 255, 255, 0)
    elif humidity >= Hmean20 + 2*Hdev20:
        print("+2sd\n")
        sense.set_pixel(1, 1, 255, 0, 0)
    elif humidity >= Hmean20 + Hdev20:
        print("+1sd\n")
        sense.set_pixel(1, 1, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(1, 1, 0, 255, 0)

    # 30 min humidity test
    print("Over the past 30 minutes, humidity is within:")
    if humidity <= Hmean30 - 2*Hdev30:
        print("-2sd\n")
        sense.set_pixel(2, 1, 255, 0, 0)
    elif humidity <= Hmean30 - Hdev30:
        print("-1sd\n")
        sense.set_pixel(2, 1, 255, 255, 0)
    elif humidity >= Hmean30 + 2*Hdev30:
        print("+2sd\n")
        sense.set_pixel(2, 1, 255, 0, 0)
    elif humidity >= Hmean30 + Hdev30:
        print("+1sd\n")
        sense.set_pixel(2, 1, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(2, 1, 0, 255, 0)

    # 10 min pressure test
    print("Over the past 10 minutes, pressure is within:")
    if pressure <= Pmean10 - 2*Pdev10:
        print("-2sd\n")
        sense.set_pixel(0, 2, 255, 0, 0)
    elif pressure <= Pmean10 - Pdev10:
        print("-1sd\n")
        sense.set_pixel(0, 2, 255, 255, 0)
    elif pressure >= Pmean10 + 2*Pdev10:
        print("+2sd\n")
        sense.set_pixel(0, 2, 255, 0, 0)
    elif pressure >= Pmean10 + Pdev10:
        print("+1sd\n")
        sense.set_pixel(0, 2, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(0, 2, 0, 255, 0)

    # 20 min pressure test
    print("Over the past 20 minutes, pressure is within:")
    if pressure <= Pmean20 - 2*Pdev20:
        print("-2sd\n")
        sense.set_pixel(1, 2, 255, 0, 0)
    elif pressure <= Pmean20 - Pdev20:
        print("-1sd\n")
        sense.set_pixel(1, 2, 255, 255, 0)
    elif pressure >= Pmean20 + 2*Pdev20:
        print("+2sd\n")
        sense.set_pixel(1, 2, 255, 0, 0)
    elif pressure >= Pmean20 + Pdev20:
        print("+1sd\n")
        sense.set_pixel(1, 2, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(1, 2, 0, 255, 0)

    # 30 min pressure test
    print("Over the past 30 minutes, pressure is within:")
    if pressure <= Pmean30 - 2*Pdev30:
        print("-2sd\n")
        sense.set_pixel(2, 2, 255, 0, 0)
    elif pressure <= Pmean30 - Pdev30:
        print("-1sd\n")
        sense.set_pixel(2, 2, 255, 255, 0)
    elif pressure >= Pmean30 + 2*Pdev30:
        print("+2sd\n")
        sense.set_pixel(2, 2, 255, 0, 0)
    elif pressure >= Pmean30 + Pdev30:
        print("+1sd\n")
        sense.set_pixel(2, 2, 255, 255, 0)
    else:
        print("mean\n")
        sense.set_pixel(2, 2, 0, 255, 0)

sched.start()