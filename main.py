#!/bin/python3

import requests
import datetime
from datasource import EcusisSource

print('   __    __   ')
print('  /  \==/  \  ')
print(' (    . .   ) ')
print('  \___   __/  ')
print('     v\ |v    ')
print('       ||     ')
print('       ,      ')
print('              ')
print(' tiny elephant')
print('     v0.1     \n')

source = EcusisSource(requests.Session())

#testdate = datetime.date.today()
testdate = datetime.date(2018, 9, 1)
print( 'Target date:', testdate, '\n')
source.get_rooms(testdate)
print("Winner winner")

testdate = datetime.date(2018, 9, 20)
print( 'Target date:', testdate, '\n')
source.get_rooms(testdate)
print("Winner winner")

testdate = datetime.date.today()
print( 'Target date:', testdate, '\n')
source.get_rooms(testdate)
print("Winner winner")
