#!/bin/python3

import requests
import datetime
from datasource import EcusisSource

#source = EcusisSource(requests.Session())
#time_slots = source.get_time_slots()

#for t in time_slots:
#    print(t)

testdate = datetime.date.today()
#testdate = datetime.date(2018, 9, 1)
print('Target date:', testdate)

source = EcusisSource(requests.Session())
#timetable = source.get_timetable()
#source.testclass()
source.testclass2(testdate)
print("Winner winner")
