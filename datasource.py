from bs4 import BeautifulSoup

class EcusisSource:
    login_url = 'https://ecusis.ecu.edu.au/ECU/login_secure.aspx'
    timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36" }
    # we should in future remove uneccesary keys from formKeys, such as weekDate
    formKeys = [ 'fromInterval', 'toInterval', 'userName', 'weekDate', '__EVENTTARGET',
        '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
        '__EVENTVALIDATION', 'pageWidth', 'txtMeetingTitle', 'selRecurInterval',
        'recurDailySpacing', 'recurWeeklySpacing', 'listToDate', 'listToMonth',
        'listToYear', 'listMonth', 'listYear']

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

    def GetHtml(self):
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
        return "".join(map(chr, r.content))
