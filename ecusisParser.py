from models import TimeSlot
from bs4 import BeautifulSoup
import time
import datetime

def is_time_format(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

def extract_week_date(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    result = soup.find('input', { 'name' : 'weekDate' })
    if (result and 'value' in result.attrs):
        return result['value']

def extract_time_slots(raw_html):
    # get the start date for this week
    weekDate = extract_week_date(raw_html)

    initialTime = datetime.datetime.strptime(weekDate, '%d %b %Y')
    time_slots = []

    soup = BeautifulSoup(raw_html, 'html.parser')
    result = soup.find('table', { 'id' : 'tblTimeTable' }) # find the timetable
    result = result.find_all('tr') # find all the rows. One per 15 min timeslot.

    for i in range(0, len(result)):
        # remove tags with no attributes, or a class of blankcell, timeHeaderHaLf or timeHeader
        thing = [tag for tag in result[i].find_all('td')
                 if (tag.attrs) and
                 (not ('class' in tag.attrs and (tag['class'] == ['blankcell'] or tag['class'] == ['timeHeaderHalf'] or tag['class'] == ['timeHeader'])))]

        # there should always be 7 left - one per day
        for j in range(0, len(thing)):
            isAvailable = 'title' in thing[j].attrs and 'class' not in thing[j].attrs and is_time_format(thing[j]['title'])

            deltaSecs = 15 * 60 * i
            delta = datetime.timedelta(j, deltaSecs)
            currentTime = initialTime + delta
            time_slots.append(TimeSlot(currentTime, datetime.timedelta(0, 15 * 60), isAvailable, ))
    return time_slots
