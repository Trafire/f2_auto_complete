from navigation import traverse
from autof2.navigation import navigation
from autof2.dailytasks import purchaselist
import datetime, time
from datetime import date
from parse import dates
from interface import keyboard, window
from database import insert_data, delete_data


def get_date_sunday(year, week):
    week -= 1
    d = str(year) + '-W' + str(week)
    return datetime.datetime.strptime(d + '-1', "%Y-W%W-%w") - datetime.timedelta(days=1)


def get_today():
    year = datetime.date.today().strftime("%Y")
    week = datetime.date.today().strftime("%W")
    day = datetime.date.today().strftime("%w")
    d = str(year) + '-W' + str(week)
    return datetime.datetime.strptime(d + '-' + day, "%Y-W%W-%w")


def go_to_puchase_list(system='f2_canada_real'):
    traverse.main_menu(system)
    for i in range(10):
        if navigation.to_purchase_list():
            return True
    return False


def get_orders(day):
    str_date = day.strftime('%d/%m/%y')
    if day >= get_today():
        print("\tprocessing day - %s" % day.strftime('%d/%m/%y'), end=" ")
        try:
            new_product = purchaselist.run_all_purchase_list_report(str_date, str_date)
        except:
            new_product = purchaselist.run_all_purchase_list_report(str_date, str_date)

        for p in new_product:
            p.date = str_date
        print(" lines found = %i" % len(new_product))
        keyboard.command('LEFT')
        return new_product
    return []
    ##            print(current.strftime('%d/%m/%y'))


def get_order_week(year, week):
    current = get_date_sunday(year, week)
    product = []
    print("\nstarting Week %i:" % week)
    for i in range(7):
        product.extend(get_orders(current))
        current += datetime.timedelta(days=1)
    print("Week %i total lines = %i" % (week, len(product)))
    return product



def clean_purchase_report_data(data):
    clean = {}
    for d in data:
        if d == 'Date':
            clean['order_date'] = dates.menu_date(data[d])
        elif d == 'Client':
            clean['client_code'] = data[d]
        elif d == 'Supplier':
            clean['supplier_code'] = data[d]
        else:
            clean[d.lower()] = data[d]
    return clean

def update_week(system, year, week):
    go_to_puchase_list(system)
    data = get_order_week(year, week)
    week_dates = dates.get_week_dates(year, week)
    products = []
    clean = []
    for d in data:
        products.append(d.all_data())
    for product in products:
        clean.append(clean_purchase_report_data(product))
    for d in week_dates:
        delete_data.delete_open_lines(system,d)
    insert_data.insert_open_lines(system, clean)


system = 'f2_canada_real'
week = 4
year = 2020
update_week(system, year, week)

'''

go_to_puchase_list()
data = get_order_week(2020, 4)
products = []
'''

clean = []
