from bs4 import BeautifulSoup
import requests
import time
import datetime
from .models import TimeSlot

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

def extract_time_slots(raw_html, room_id):
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
            isAvailable = 'class' in thing[j].attrs and thing[j]['class'] == ["available"]

            # TODO for some reason times seem to be starting at 00:15 when they should be starting at 00:00
            deltaSecs = 15 * 60 * i
            delta = datetime.timedelta(j, deltaSecs)
            currentTime = initialTime + delta

            title = thing[j]['title']
            classText = thing[j]['class']

            time_slots.append(TimeSlot(currentTime, 15 * 60, isAvailable, str(title) + str(classText), room_id))
    return time_slots

class EcusisSource:
    login_url = 'https://ecusis.ecu.edu.au/ECU/login_secure.aspx'
    timetable_url = "https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code="
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36" }
    # we should in future remove uneccesary keys from formKeys, such as weekDate
    formKeys = [ 'fromInterval', 'toInterval', 'userName', 'weekDate', '__EVENTTARGET',
        '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
        '__EVENTVALIDATION', 'pageWidth', 'txtMeetingTitle', 'selRecurInterval',
        'recurDailySpacing', 'recurWeeklySpacing', 'listToDate', 'listToMonth',
        'listToYear', 'listMonth', 'listYear']

    def __login(self, username, password):
        payload = {
            'txtUserName' : username,
            'txtPassword' : password,
            'btnLogin' : 'Login',
            '__VIEWSTATE' : '/wEPDwUJNzYxMTIyMTIwZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUNY2hrUmVtZW1iZXJNZba2id2ChWAsS0mmMejEzXWOpThvq+sk82BQ79XoGjsZ',
            '__VIEWSTATEGENERATOR' : '4C3AC411',
            '__EVENTVALIDATION' : '/wEdAAX4xJakxGm2npWRNdxo4ICaY3plgk0YBAefRz3MyBlTcFvv90Pojif5f4vmhiSDFhd2NvjHOkq5wKoqN6Aim8WGop4oRunf14dz2Zt2+QKDEBm9vSQW1ejyO5kJ9lZijHHpigrR7VfQfDhT5Eaef4/F'
        }
        self.session.post(self.login_url, data = payload, headers = self.headers)

    def __init__(self, username, password):
        self.session = requests.Session()
        self.__login(username, password)

    def __getvalue(self, input_form_element, soup):
        result = soup.find('input', attrs={'name': input_form_element})
        if result:
            return result.get('value', '')
        return ''

    def get_time_slots(self, room_id):
        # initial request to page - we need to make this before we can make a request
        # date, for some reason.
        payload = {'pageWidth' : '1200'}
        url = self.timetable_url + room_id

        r = self.session.post(url, data = payload, headers = self.headers)
        # construct the next post request using the viewstate etc from that page
        # TODO: check for a 404 response here.

        soup = BeautifulSoup(r.content, 'html.parser')
        payload = {}
        for key in self.formKeys:
            payload[key] = self.__getvalue(key, soup)

        # the date is a integer stored as a string in __EVENTARGUMENT
        # where 01 Jan 2000 = 0 (or 1, I'll do the maths later)
        #
        # The date must clickable on the calendar of the current date
        # any date outside of the range of the calendar will 404
        payload['__EVENTTARGET'] = 'calendar'
        payload['__EVENTARGUMENT'] = '6592'

        # these keys must be populated with valid values but do not need to match __EVENTARGUMENT
        payload['selRecurInterval'] = 'Weekly'
        payload['listToMonth'] = 'Mar'
        payload['listToYear'] = '2019'
        payload['listMonth'] = 'March'
        payload['listYear'] = '2019'

        # weekDate is uneccesary and can be empty
        #payload['weekDate'] = ''

        r = self.session.post(url, data = payload, headers = self.headers)
        html_str = "".join(map(chr, r.content))
        return extract_time_slots(html_str, room_id)
