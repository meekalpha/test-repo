<<<<<<< HEAD
#!/bin/python3

import requests
from bs4 import BeautifulSoup
import re

timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36" }


session = requests.Session()
r = session.post(timetable_url, data = payload, headers = headers)
=======
import ecusisUtils
import datetime

test = datetime.date(2018, 1, 1)
today = datetime.date.today()

u = ecusisUtils

print("Test date:", u.dmy_to_ecusisdate(test))
print("Last day of the calendar:", u.last_day_on_calendar(test))
print("Last day of the calendar (today):", u.last_day_on_calendar(today))
print("In current calendar?:", u.is_target_on_calendar(today, test))

test = [datetime.date.today(),
        datetime.date(2018, 1, 1),
        datetime.date(2018, 2, 4),
        datetime.date(2018, 3, 30),
        datetime.date(2018, 4, 1),
        datetime.date(2018, 4, 19),
        datetime.date(2018, 9, 9),
        datetime.date(2018, 10, 1),
        datetime.date(2018, 10, 22),
        datetime.date(2019, 1, 1),
        datetime.date(2019, 10, 3)]

test2 = []

print('=== dmy_to_ecusisdate ===')
for date in test:
    ecusis = u.dmy_to_ecusisdate(date)
    print(date, '-> ', ecusis)
    test2.append(ecusis)

print('=== ecusisdate_to_dmy ===')
for date in test2:
    print(date, '-> ', u.ecusisdate_to_dmy(date))

print('=== last_day_on_calendar ===')
for date in test:
    print(date, '-> ', u.last_day_on_calendar(date))

print('=== is_target_on_calendar ===')
for date in test:
    print(date, '-> ', u.is_target_on_calendar(today, date))
>>>>>>> fbcfa09a956ba0ba142c98b2e9d4c91dc158d6e6
