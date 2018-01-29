import ecusisUtils
import datetime

test = datetime.date(2018, 1, 1)
today = datetime.date.today()

u = ecusisUtils

print("Test date:", u.dmy_to_ecusisdate(test))
print("Last day of the calendar:", u.last_day_on_calendar(test))
print("Last day of the calendar (today):", u.last_day_on_calendar(today))
print("In current calendar?:", u.is_target_on_calendar(test))

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
    print(date, '-> ', u.is_target_on_calendar(date))
