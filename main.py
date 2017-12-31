#!/bin/python3

import requests
from bs4 import BeautifulSoup

login_url = 'https://ecusis.ecu.edu.au/ECU/login_secure.aspx'
timetable_url = 'https://ecusis.ecu.edu.au/roomBookings/timetable.aspx?loc_code=200012227'
#r = requests.get()

session = requests.Session()


f = open('credentials\password.txt', 'r')
pw = f.readline()

payload = {'txtUserName' : 'jrospond',
            'txtPassword' : pw,
            'btnLogin' : 'Login',
            '__VIEWSTATE' : '/wEPDwUJNzYxMTIyMTIwZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUNY2hrUmVtZW1iZXJNZba2id2ChWAsS0mmMejEzXWOpThvq+sk82BQ79XoGjsZ',
            '__VIEWSTATEGENERATOR' : '4C3AC411',
            '__EVENTVALIDATION' : '/wEdAAX4xJakxGm2npWRNdxo4ICaY3plgk0YBAefRz3MyBlTcFvv90Pojif5f4vmhiSDFhd2NvjHOkq5wKoqN6Aim8WGop4oRunf14dz2Zt2+QKDEBm9vSQW1ejyO5kJ9lZijHHpigrR7VfQfDhT5Eaef4/F'
            }

r = session.post(login_url, data = payload)

print (r.cookies.get_dict())
print (r.status_code)
print (r.url)


payload = {'__EVENTTARGET' : 'calendar', '__EVENTARGUMENT' : '6504'}
payload = {'pageWidth' : '1200'}
#payload = {'pageWidth' : '1200', '__EVENTTARGET' : 'calendar', '__EVENTARGUMENT' : '6504'}
#payload = ttViewRequest.get_request()
#r = session.get(timetable_url, data = calendar)




r = session.post(timetable_url, data = payload)
#print (r.content)


byte = r.content
f = open('output/out.html','w')
html_doc = "".join(map(chr, byte))
f.write(html_doc)
f.close()


soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())


def getDataFor(input_form_element):
    result = soup.find('input', attrs={'name': input_form_element})
    if result:
        return result.get('value', '')
    return ''

formKeys = [
    'fromInterval',
    'toInterval',
    'userName',
    'weekDate',
    '__EVENTTARGET',
    '__EVENTARGUMENT',
    '__LASTFOCUS',
    '__VIEWSTATE',
    '__VIEWSTATEGENERATOR',
    '__EVENTVALIDATION',
    'pageWidth',
    'txtMeetingTitle',
    'selRecurInterval',
    'recurDailySpacing',
    'recurWeeklySpacing',
    'listToDate',
    'listToMonth',
    'listToYear',
    'listMonth',
    'listYear']

'''
payload = {}
for key in formKeys:
    payload[key] = getDataFor(key)

payload['__EVENTARGUMENT'] = 'listMonth'
payload['selRecurInterval'] = 'Weekly'
payload['listToMonth'] = 'Jan'
payload['listToYear'] = '2017'
payload['listMonth'] = 'July'
payload['listYear'] = '2018'
payload['weekDate'] = '4 Dec 2017'

r = session.post(timetable_url, data = payload)
'''

payload = {}
for key in formKeys:
    payload[key] = getDataFor(key)
payload['__EVENTARGUMENT'] = 'calendar'
payload['__EVENTTARGET'] = '6376'
payload['selRecurInterval'] = 'Weekly'
payload['listToMonth'] = 'Jan'
payload['listToYear'] = '2017'
payload['listMonth'] = 'June'
payload['listYear'] = '2017'
payload['weekDate'] = '4 Dec 2017'
r = session.post(timetable_url, data = payload)
print (r.request.body)
#print (r.content)

byte = r.content
f = open('output/out2.html','w')
html_doc = "".join(map(chr, byte))
f.write(html_doc)
f.close()


'''

print (payload['weekDate'])
print (payload['userName'])
print (payload['toInterval'])
print (payload['fromInterval'])
'''
