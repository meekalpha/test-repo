#!/bin/python3

import requests
from bs4 import BeautifulSoup
import re

timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36" }


session = requests.Session()
r = session.post(timetable_url, data = payload, headers = headers)
