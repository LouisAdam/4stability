#!/usr/bin/python
from optparse import OptionParser
import os
import sys
import time
import csv
import datetime

import motor
import adxl345
import hcsr04

#parser = OptionParser()
#parser.add_option("-p", "--p", dest="p", help="")
#(options, args) = parser.parse_args()

m = motor.Motor(debug=False)
dist = hcsr04.HCSR04()

m.init()

def experiment(bwrate, range, max_speed):
	try:
		print 'start experiment:'+str(bwrate)+'@'+str(range)
		lines = []
		speed_percent = 0.0
		start_timeout = None
		accel = adxl345.ADXL345(bwrate=bwrate, range=range)
		while (True):
			distance = 0 #dist.measure()
			axis = accel.getAxes()

			if start_timeout is None:
				speed_percent += 0.2
			if speed_percent > max_speed: # max 34
				start_timeout = time.time()
				#break
			if time.time() - start_timeout > 5:
				break
			print speed_percent
			pos = m.set_speed(speed_percent/100.0)

			ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f')

			line = []
			line.append(ts)
			line.append(round(speed_percent,2))
			line.append(axis['x'])
			line.append(axis['y'])
			line.append(axis['z'])

			line.append(round(distance,2))

			line.append(pos)
			lines.append(line)
			time.sleep(0.1)
	except Exception as e:
		print e
	finally:
		pos = m.set_speed(0)
		header = ["datetime", "speed", "x", "y", "z", "d", "speed_real"]
		ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S_%f')
		with open('results/'+ts+'_'+str(max_speed)+'-'+str(bwrate)+'@'+str(range)+'.csv', 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter='	', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(header)
			for line in lines:
				spamwriter.writerow(line)

#bwrates = [adxl345.ADXL345.BW_RATE_1600HZ, adxl345.ADXL345.BW_RATE_800HZ, adxl345.ADXL345.BW_RATE_200HZ, adxl345.ADXL345.BW_RATE_100HZ, adxl345.ADXL345.BW_RATE_50HZ, adxl345.ADXL345.BW_RATE_25HZ]
bwrates = [adxl345.ADXL345.BW_RATE_1HZ, adxl345.ADXL345.BW_RATE_01HZ]
#ranges = [adxl345.ADXL345.RANGE_2G, adxl345.ADXL345.RANGE_4G, adxl345.ADXL345.RANGE_8G, adxl345.ADXL345.RANGE_16G]
ranges = [adxl345.ADXL345.RANGE_2G]
for bwrate in bwrates:
	for range in ranges:
		#experiment(bwrate, range, 47)
		experiment(bwrate, range, 34)
		time.sleep(3)

m.reset()

