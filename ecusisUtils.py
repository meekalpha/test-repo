import datetime

ecusis_epoch_ordinal = 730120
today = datetime.date.today()

# Converts datetime.date object to ECUSIS ordinal
# Receives datetime.date and returns int
def dmy_to_ecusisdate(input_date):
    input_date_ordinal = input_date.toordinal()
    input_date_ecusis = input_date_ordinal - ecusis_epoch_ordinal
    return input_date_ecusis

# Converts ECUSIS ordinal to datetime.date object
# Receives int and returns datetime.date
def ecusisdate_to_dmy(input_date_ecusis):
    input_date_ordinal = input_date_ecusis + ecusis_epoch_ordinal
    input_date = datetime.date.fromordinal(input_date_ordinal)
    return input_date

# Calculates the last date on ECUSIS calendar for a given date, returns ECUSIS ordinal
# Receives datetime.date object and returns int
def last_day_on_calendar(input_date):
    # find first day of the current month
    first_day_month = input_date.replace(day=1)
    first_day_month_ecusis = dmy_to_ecusisdate(first_day_month)
    # calculate first day shown on the calendar
    # Note: mod 7 == 2 for any given Monday
    first_day_calendar_ecusis = first_day_month_ecusis - ((first_day_month_ecusis - 2) % 7)
    # calculate last day shown on the calendar
    last_day_ecusis = first_day_calendar_ecusis + 41
    # check if January 1 is a Monday (has one less week shown)
    if first_day_month_ecusis % 7 == 2:
        last_day_ecusis -= 7
    return last_day_ecusis

# Determines if the target date is clickable on the ECUSIS calendar
# Receives datetime.date object and returns bool
def is_target_on_calendar(target_date):
    on_calendar = True
    target_date_ecusis = dmy_to_ecusisdate(target_date)
    if target_date_ecusis > last_day_on_calendar(today):
        on_calendar = False
    return on_calendar
