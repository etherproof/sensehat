# -*- coding: utf-8 -*-
"""
Created on Sun May 21 16:52:01 2017

@author: pi
"""
# Import relevant libraries
from sense_hat import SenseHat
sense = SenseHat()

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

# Take readings every 60 seconds
@sched.scheduled_job('interval', seconds=60)
def timed_job():
    # Take readings
    humidity = sense.get_humidity()
    temp = sense.get_temperature()
    pressure = sense.get_pressure()

    # Print readings to terminal
    print(str(datetime.now()))
    print("Temperature:\t %s C" % round(temp, 1))
    print("Humidity:\t %s %%rH" % round(humidity, 1))
    print("Pressure:\t %s Millibars\n" % round(pressure, 1))

    # Write (append) readings to CSV.
    f= open("climate.csv", "a+")
    f.write("%s, %f, %f, %f \n" % (datetime.now(), temp, humidity, pressure))
    f.close()
sched.start()