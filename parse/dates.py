from datetime import datetime, timedelta


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


def menu_date(date_str):
    return datetime.strptime(date_str, '%d/%m/%y')


def database_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')


# datetime to string/int

def get_time(datetime_object):
    return datetime_object.strftime('%H%M')


def get_menu_date(date_object):
    return date_object.strftime('%d/%m/%y')


def get_week(date_object):
    return date_object.isocalendar()[:2][1]


def get_year(date_object):
    return int(date_object.year)


def get_database_date(date_object):
    return date_object.strftime('%Y-%m-%d')


def get_pricing_week(date_object):
    if date_object.weekday() > 3:
        date_object = date_object + timedelta(weeks=1)
    return get_week(date_object)


def get_pricing_year(date_object):
    if date_object.weekday() > 3:
        date_object = date_object + timedelta(weeks=1)
    return get_year(date_object)


def get_date_of_weekday(year, week, day):
    day = day.lower()
    day_num = {
        'sunday': 0,
        'sun': 0,
        'monday': 1,
        'mon': 1,
        'tuesday': 2,
        'tue': 2,
        'wednesday': 3,
        'wed': 3,
        'thursday': 4,
        'thu': 4,
        'friday': 5,
        'fri': 5,
        'saturday': 6,
        'sat': 6
    }
    sunday = get_date_sunday(year, week)

    return sunday + timedelta(days=day_num[day])


def get_current_week():
    n = datetime.now()
    return (get_year(n), get_week(n))
