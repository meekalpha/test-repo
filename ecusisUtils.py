import datetime
#import calendar

ecusis_epoch_ordinal = 730120
today = datetime.date.today()

# Converts datetime.date object to ECUSis ordinal
# Receives datetime.date and returns int
def dmy_to_ecusisdate(input_date):
    input_date_ordinal = input_date.toordinal()
    input_date_ecusis = input_date_ordinal - ecusis_epoch_ordinal
    return input_date_ecusis

# Converts ECUSis ordinal to datetime.date object
# Receives int and returns datetime.date
def ecusisdate_to_dmy(input_date):
    input_date_ordinal = input_date + ecusis_epoch_ordinal
    input_date_dmy = datetime.date.fromordinal(input_date_ordinal)
    return input_date_dmy

# Calculates the last date on ECUSis calendar for a given date, returns ECUSis ordinal
# Receives datetime.date object and returns int
def last_day_calendar_ecusis(input_date):
    first_day_month = input_date.replace(day=1)
    first_day_month_ecusis = dmy_to_ecusisdate(first_day_month)
    first_day_calendar_ecusis = first_day_month_ecusis - ((first_day_month_ecusis - 2) % 7)
    last_day_calendar_ecusis = first_day_calendar_ecusis + 41
    if first_day_month_ecusis % 7 == 2:
        last_day_calendar_ecusis -= 7
#    if first_day_month.weekday == 0:
#        last_day_calendar_ecusis -= 7
    return last_day_calendar_ecusis

##### Not working #####
# Calculates the last date on ECUSis calendar for a given date, returns ECUSis ordinal
# Receives datetime.date object and returns int
def last_day_calendar_ecusis_old(input_date):
    days_in_current_month = calendar.mdays[input_date.month]
    lastd_month = input_date.replace(day=days_in_current_month)
    lastd_month_ecusis = dmy_to_ecusisdate(lastd_month)
    lastd_calendar_ecusis = lastd_month_ecusis + 8 - ((lastd_month_ecusis - 2) % 7)
    return lastd_calendar_ecusis

# Determines if the target date is clickable on the ECUSis calendar
# Receives datetime.date object and returns bool
def is_target_in_calendar(target_date):
    in_calendar = True
    target_date_ecusis = dmy_to_ecusisdate(target_date)
    if target_date_ecusis > last_day_calendar_ecusis(today):
        in_calendar = False
    return in_calendar


test = datetime.date(2018, 1, 1)
print("Test date:", dmy_to_ecusisdate(test))
print("Last day of the calendar:", last_day_calendar_ecusis(test))
print("Last day of the calendar (today):", last_day_calendar_ecusis(today))
print("In current calendar?:", is_target_in_calendar(test))
