from ecusisParser import extract_time_slots
from bs4 import BeautifulSoup
from ecusisUtils import is_target_in_week, is_target_on_calendar, dmy_to_ecusisdate, ecusisdate_to_dmy
import datetime

class EcusisSource:
    current_date = datetime.date.today()
    login_url = 'https://ecusis.ecu.edu.au/ECU/login_secure.aspx'
    timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    # we should in future remove uneccesary keys from formKeys, such as weekDate
    #formKeys = [ 'fromInterval', 'toInterval', 'userName', 'weekDate', '__EVENTTARGET',
    #    '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
    #    '__EVENTVALIDATION', 'pageWidth', 'txtMeetingTitle', 'selRecurInterval',
    #    'recurDailySpacing', 'recurWeeklySpacing', 'listToDate', 'listToMonth',
    #    'listToYear', 'listMonth', 'listYear']

    formKeys = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']

    rooms = {
        '200011101' : ('1.101', 0, 0, 0, 1, 'Handa Studio (percussion)'),
        '200011117' : ('1.117', 0, 0, 0, 0, 'Practice Room'),
        '200011119' : ('1.119', 0, 0, 0, 0, 'Practice Room (upright piano)'),
        '200011123' : ('1.123', 0, 0, 0, 0, 'Practice Room'),
        '200011124' : ('1.124', 0, 0, 0, 0, 'Practice Room (wood floor)'),
        '200011125' : ('1.125', 0, 0, 0, 0, 'Practice Room (double)'),
        '200011127' : ('1.127', 0, 0, 1, 1, 'Jazz Drum Room'),
        '200011129' : ('1.129', 0, 0, 1, 1, 'Contemporary Drum Room'),
        '200011130' : ('1.130', 0, 0, 0, 0, 'Practice Room'),
        '200011131' : ('1.131', 0, 0, 0, 0, 'Practice Room (no piano)'),
        '200011132' : ('1.132', 0, 0, 0, 0, 'Practice Room (wood floor)'),
        '200011133' : ('1.133', 0, 0, 0, 0, 'Practice Room'),
        '200011139' : ('1.139', 0, 0, 0, 0, 'Voice Room 2'),
        '200011141' : ('1.141', 0, 0, 0, 0, 'Practice Room (no piano, no window)'),
        '200011142' : ('1.142', 0, 0, 0, 0, 'Practice Room (no piano, no window)'),
        '200011143' : ('1.143', 1, 1, 1, 0, 'Ensemble Room 6 (keyboard only)'),
        '200011145' : ('1.145', 1, 1, 1, 0, 'Ensemble Room 7 (keyboard only)'),
        '200012202' : ('1.202', 0, 0, 0, 0, 'Sound Control Room'),
        '200012208' : ('1.208', 1, 1, 1, 0, 'Ensemble Studio 1'),
        '200012209' : ('1.209', 1, 1, 1, 0, 'Ensemble Studio 2'),
        '200012210' : ('1.210', 0, 0, 0, 0, 'Practice Room (no window)'),
        '200012216' : ('1.216', 0, 0, 0, 0, 'Practice Room (piano)'),
        '200012217' : ('1.217', 0, 0, 0, 0, 'Practice Room (piano, wood floor)'),
        '200012218' : ('1.218', 0, 0, 0, 0, 'Practice Room (wood floor)'),
        '200012219' : ('1.219', 1, 1, 1, 0, 'Ensemble Studio 5'),
        '200012227' : ('1.227', 1, 1, 1, 0, 'Ensemble Studio 4'),
        '200012228' : ('1.228', 0, 0, 0, 0, 'Movement Studio 1 (wood floor)'),
        '200012234' : ('1.234', 0, 0, 0, 0, 'Practice Room (no piano, no window)'),
        '200012236' : ('1.236', 1, 1, 1, 0, 'Jazz Studio')
    }

#    rooms = {
#        '200011101' : ('1.101', 0, 0, 0, 1, 'Handa Studio (percussion)'),
#        '200011117' : ('1.117', 0, 0, 0, 0, 'Practice Room')}

    def __login(self):
        f = open('credentials\password.txt', 'r')
        pw = f.readline()
        f.close()
        payload = {
            'txtUserName' : 'jrospond',
            'txtPassword' : pw,
            'btnLogin' : 'Login',
            '__VIEWSTATE' : '/wEPDwUJNzYxMTIyMTIwZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUNY2hrUmVtZW1iZXJNZba2id2ChWAsS0mmMejEzXWOpThvq+sk82BQ79XoGjsZ',
            '__VIEWSTATEGENERATOR' : '4C3AC411',
            '__EVENTVALIDATION' : '/wEdAAX4xJakxGm2npWRNdxo4ICaY3plgk0YBAefRz3MyBlTcFvv90Pojif5f4vmhiSDFhd2NvjHOkq5wKoqN6Aim8WGop4oRunf14dz2Zt2+QKDEBm9vSQW1ejyO5kJ9lZijHHpigrR7VfQfDhT5Eaef4/F'
        }
        self.session.post(self.login_url, data = payload, headers = self.headers)

    def __init__(self, session):
        self.session = session
        self.__login()

    def __getvalue(self, input_form_element, soup):
        value = ''
        result = soup.find('input', attrs={'name': input_form_element})
        if result:
            value = result.get('value', '')
        return value

    def __write_to_file(self, filename, soup):
        f = open('output/%s.html' % filename, 'w')
        f.write("".join(map(chr, soup.content)))
        f.close()

    def __parse_viewstate(self, soup):
        soup = BeautifulSoup(soup.content, 'html.parser')
        payload = {}
        for key in self.formKeys:
            payload[key] = self.__getvalue(key, soup)
        return payload

    def __select_date(self, target_date):
        calendar_check = is_target_on_calendar(self.current_date, target_date)
        week_check = is_target_in_week(self.current_date, target_date)

        print('>> Checking target date')
        print(' On current calendar? ...', calendar_check)
        print(' In current week? ...', week_check)

        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
        payload = {'pageWidth' : '1200'}

        if calendar_check == False or week_check == False:
            print(' Date change required')
            print(' Initial request ... ', end = '', flush=True)
            r = self.session.post(timetable_url, data = payload, headers = self.headers)
            payload.update(self.__parse_viewstate(r))
            print('DONE')
        else:
            print(' Date change not required')

        if calendar_check == False:
            print(' Changing calendar to ', end = '', flush=True)
            payload['__EVENTTARGET'] = 'listMonth'
            payload['__EVENTARGUMENT'] = ''
            payload['listMonth'] = target_date.strftime("%B")
            payload['listYear'] = target_date.strftime("%Y")
            # these keys must be populated with valid values but do not need to match __EVENTARGUMENT
            payload['selRecurInterval'] = 'Weekly'
            payload['listToMonth'] = 'Jan'
            payload['listToYear'] = '2018'
            print(payload['listMonth'], payload['listYear'], '... ', end = '', flush=True)
            r = self.session.post(timetable_url, data = payload, headers = self.headers)
            payload.update(self.__parse_viewstate(r))
            self.__write_to_file('change_cal', r)
            print('DONE')

        if week_check == False:
            print(' Changing week to ', end = '', flush=True)
            target_date_ecusis = dmy_to_ecusisdate(target_date)
            payload['__EVENTTARGET'] = 'calendar'
            payload['__EVENTARGUMENT'] = str(target_date_ecusis)
            print(payload['__EVENTARGUMENT'], '... ', end = '', flush=True)
            r = self.session.post(timetable_url, data = payload, headers = self.headers)
            payload.update(self.__parse_viewstate(r))
            self.__write_to_file('change_week', r)
            print('DONE')

        print(' Date change successful.\n')

    def __select_rooms(self):
        # will in future construct a list/dict with all desired rooms
        print('>> Selecting rooms')
        selection = self.rooms
        print('Selection complete.\n')
        return selection

    def get_rooms(self, target_date):
        rooms = self.__select_rooms()
        self.__select_date(target_date)
        payload = {'pageWidth' : '1200'}

        print('>> Requesting timetables')

        for key in rooms.keys():
            print(' Requesting', rooms[key][0], '... ', end = '', flush=True)
            timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=%s'  % key
            r = self.session.post(timetable_url, data = payload, headers = self.headers)
            self.__write_to_file(key, r)
            print('DONE')

        print(' Requests complete.\n')

    def get_time_slots(self):
        # initial request to page - we need to make this before we can make a request
        # date, for some reason.
        payload = {'pageWidth' : '1200'}
        r = self.session.post(self.timetable_url, data = payload, headers = self.headers)

        # construct the next post request using the viewstate etc from that page
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
        payload['__EVENTARGUMENT'] = '6610'

        # these keys must be populated with valid values but do not need to match __EVENTARGUMENT
        payload['selRecurInterval'] = 'Weekly'
        payload['listToMonth'] = 'Mar'
        payload['listToYear'] = '2019'
        payload['listMonth'] = 'March'
        payload['listYear'] = '2019'

        # weekDate is uneccesary and can be empty
        #payload['weekDate'] = ''

        r = self.session.post(self.timetable_url, data = payload, headers = self.headers)
        html_str = "".join(map(chr, r.content))
        return extract_time_slots(html_str)
