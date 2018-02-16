#!/bin/python3

import requests
import datetime
from datasource import EcusisSource

testdate = datetime.date.today()
testdate = datetime.date(2018, 9, 1)
print('Target date:', testdate)


source = EcusisSource(requests.Session())
source.test_bed(testdate)
print("Winner winner")
