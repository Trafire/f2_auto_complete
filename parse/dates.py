from datetime import datetime

def lot_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%y')

def get_week(date_object):
    return date_object.isocalendar()[:2][1]

def get_year(date_object):
    return str(date_object.year)


#a = lot_date('13-12-19')
#print(get_week(a))