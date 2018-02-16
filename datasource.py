from ecusisParser import extract_time_slots
from bs4 import BeautifulSoup
from ecusisUtils import is_target_in_week, is_target_on_calendar, dmy_to_ecusisdate, ecusisdate_to_dmy
import datetime

class EcusisSource:
    current_date = datetime.date.today()
    login_url = 'https://ecusis.ecu.edu.au/ECU/login_secure.aspx'
    timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36" }
    # we should in future remove uneccesary keys from formKeys, such as weekDate
    #formKeys = [ 'fromInterval', 'toInterval', 'userName', 'weekDate', '__EVENTTARGET',
    #    '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
    #    '__EVENTVALIDATION', 'pageWidth', 'txtMeetingTitle', 'selRecurInterval',
    #    'recurDailySpacing', 'recurWeeklySpacing', 'listToDate', 'listToMonth',
    #    'listToYear', 'listMonth', 'listYear']
    formKeys = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']

    def __login(self):
        f = open('credentials\password.txt', 'r')
        pw = f.readline()
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
        result = soup.find('input', attrs={'name': input_form_element})
        if result:
            return result.get('value', '')
        return ''

    def testclass(self):
        payload = {'pageWidth' : '1200'}

        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'

        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out227.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        # construct the next post request using the viewstate etc from that page
        soup = BeautifulSoup(r.content, 'html.parser')
        payload = {}
        for key in self.formKeys:
            payload[key] = self.__getvalue(key, soup)


        payload['__EVENTTARGET'] = 'listMonth'
        payload['__EVENTARGUMENT'] = ''
        payload['listMonth'] = 'April'
        payload['listYear'] = '2018'
        # these keys must be populated with valid values but do not need to match __EVENTARGUMENT
        payload['selRecurInterval'] = 'Weekly'
        payload['listToMonth'] = 'Jan'
        payload['listToYear'] = '2018'

        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out227_apr.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        # construct the next post request using the viewstate etc from that page
        soup = BeautifulSoup(r.content, 'html.parser')
        payload = {}
        for key in self.formKeys:
            payload[key] = self.__getvalue(key, soup)

        payload['__EVENTTARGET'] = 'calendar'
        payload['__EVENTARGUMENT'] = '6694'

        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out227_apr30.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()

        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012208'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out208_apr30.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()

    #def __select_date(self, target_date):
    def testclass2(self, target_date):
        calendar_check = is_target_on_calendar(self.current_date, target_date)
        print('>>>> Checking target date')
        print('>> Calendar check -', calendar_check)
        week_check = is_target_in_week(self.current_date, target_date)
        print('>> Week check -', week_check)

        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
        payload = {'pageWidth' : '1200'}

        if calendar_check == False or week_check == False:
            print('>> Date change required')
            print('>> Initialising ...', end = '')
            r = self.session.post(timetable_url, data = payload, headers = self.headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            payload = {}
            for key in self.formKeys:
                payload[key] = self.__getvalue(key, soup)
            print('DONE')

        if calendar_check == False:
            print('>> Changing calendar ...', end = '')
            payload['__EVENTTARGET'] = 'listMonth'
            payload['__EVENTARGUMENT'] = ''
            payload['listMonth'] = target_date.strftime("%B")
            payload['listYear'] = target_date.strftime("%Y")

            # these keys must be populated with valid values but do not need to match __EVENTARGUMENT
            payload['selRecurInterval'] = 'Weekly'
            payload['listToMonth'] = 'Jan'
            payload['listToYear'] = '2018'
            print(payload['listMonth'], payload['listYear'], '...', end = '')

            r = self.session.post(timetable_url, data = payload, headers = self.headers)

            # construct the next post request using the viewstate etc from that page
            soup = BeautifulSoup(r.content, 'html.parser')
            payload = {}
            for key in self.formKeys:
                payload[key] = self.__getvalue(key, soup)

            f = open('output/out_month.html', 'w')
            f.write("".join(map(chr, r.content)))
            f.close()

            print('DONE')

        if week_check == False:
            print('>> Changing week ...', end = '')
            target_date_ecusis = dmy_to_ecusisdate(target_date)
            payload['__EVENTTARGET'] = 'calendar'
            payload['__EVENTARGUMENT'] = str(target_date_ecusis)
            print(payload['__EVENTARGUMENT'], '...', end = '')

            r = self.session.post(timetable_url, data = payload, headers = self.headers)

            # construct the next post request using the viewstate etc from that page
            soup = BeautifulSoup(r.content, 'html.parser')
            payload = {}
            for key in self.formKeys:
                payload[key] = self.__getvalue(key, soup)

            f = open('output/out_week.html', 'w')
            f.write("".join(map(chr, r.content)))
            f.close()

            print('DONE')

        print('>> Check complete')

    #def testclass2(self, target_date):

        #self.__select_date(target_date)

        print('>>>> Requesting timetables')
        payload['pageWidth'] = '1200'

        print('>> Requesting 227 ...', end = '')
        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out227.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        print('DONE')

        print('>> Requesting 208 ...', end = '')
        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012208'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out208.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        print('DONE')

        print('>> Requesting 219 ...', end = '')
        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012219'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out219.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        print('DONE')

        print('>> Requesting 236 ...', end = '')
        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012236'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out236.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        print('DONE')

        print('>> Requesting 236 ...', end = '')
        timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200011123'
        r = self.session.post(timetable_url, data = payload, headers = self.headers)
        f = open('output/out123.html', 'w')
        f.write("".join(map(chr, r.content)))
        f.close()
        print('DONE')

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
