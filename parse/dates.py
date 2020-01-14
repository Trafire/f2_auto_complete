from datetime import datetime,timedelta

## string to datetime

def get_date_sunday(year, week):
    week -= 1
    d = str(year) + '-W' + str(week)
    return datetime.strptime(d + '-1', "%Y-W%W-%w") - timedelta(days=1)

def get_week_dates(year, week):
    week = [get_date_sunday(year, week)]
    for i in range(6):
        week.append(week[-1] + timedelta(days=1))
    return week


def lot_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%y')

def menu_date (date_str):
    return datetime.strptime(date_str, '%d/%m/%y')

def database_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')
# datetime to string/int

def get_menu_date(date_object):
    return date_object.strftime('%d/%m/%y')

def get_week(date_object):
    return date_object.isocalendar()[:2][1]

def get_year(date_object):
    return str(date_object.year)

def get_database_date(date_object):
    return date_object.strftime('%Y-%m-%d')

