#!/usr/bin/env python
import os, sys, re
import os
from array import array
import ROOT

## This function reads a fill report and returns a list of fill start and end times, in seconds (measured by TTimeStamp relative to Jan 1, 1970 00:00:00 UTC)
outFile = open("processedFillList2018.txt","w")
import csv
reader = csv.reader(open("rawFillList2018.txt"))

if True:
	for fill in sorted(reader):
#with open("rawFillList2018.txt") as fills:
#	for fill in fills:
		#print fill
		if "LHCFILL" in fill or len(fill) < 4:
			#print "skipping"
			continue

		#print "length ",len(fill)
	#	print "\tFill ",fill[0], ", start time ",fill[1],", end time ",fill[2],"lumi",fill[3],"party 1",fill[4],"party 2",fill[5]

		fillNum =fill[0].strip()
		fillLumi = fill[3].strip()		
		# party1 = fill[4].strip()
		# party2 = fill[5].strip()

		###Now this check is done in previous stage
		# if party1 != "1" or party2 != "1": 
		# 	continue #not p-p collisions

		startDate = fill[1]
		year = int(startDate.split("-")[0])
		month = int(startDate.split("-")[1])
		day = int(startDate.split("-")[2].split(" ")[0])
		startTimeList = startDate.split(" ")[1].split(":")
		hours = int(startTimeList[0])#hours
		minutes = int(startTimeList[1])#minutes
		seconds =int(startTimeList[2])#seconds

		#print startDate,startTimeList,year,month,day,hours,minutes,seconds
		#Fill report times are in UTC
		startTime=ROOT.TTimeStamp(year,month,day,hours,minutes,seconds)

		endDate = fill[2]
		if endDate != "":
			year = int(endDate.split("-")[0])
			month = int(endDate.split("-")[1])
			day = int(endDate.split("-")[2].split(" ")[0])
			endTimeList = endDate.split(" ")[1].split(":")
			hours = int(endTimeList[0])#hours
			minutes = int(endTimeList[1])#minutes
			seconds =int(endTimeList[2])#seconds

			#print endDate,endTimeList,year,month,day,hours,minutes,seconds
			endTime=ROOT.TTimeStamp(year,month,day,hours,minutes,seconds)

			duration = round((endTime.GetSec()-startTime.GetSec())/3600.,1) ##hrs
			avg_lumi = float(fillLumi)/duration ### pb-1/hr
		
		     	#		print duration,"hours"
			outFile.write("%s %s %s %s %s %0.2f\n" % (fillNum, str(startTime.GetSec()),str(endTime.GetSec()),fillLumi,startDate,avg_lumi))
			#outFile.write("%s %s %s %s %s\n" % (fillNum, str(startTime.GetSec()),str(endTime.GetSec()),fillLumi,startDate))
		else: ##ongoing fill
	#		print "ongoing"
			#outFile.write("%s %s %s %s %s\n" % (fillNum, str(startTime.GetSec()),"-1",fillLumi,startDate))
			now = ROOT.TTimeStamp()##
			duration = round((now.GetSec()-startTime.GetSec())/3600.,1)
			avg_lumi = float(fillLumi)/duration
			outFile.write("%s %s %s %s %s %0.2f\n" % (fillNum, str(startTime.GetSec()),"-1",fillLumi,startDate,avg_lumi))

		
