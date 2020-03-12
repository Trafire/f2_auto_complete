import datetime
import time

import pandas as pd

from database import insert_data, update_data, get_data
from interface import keyboard
from interface import window
from parse import lots, dates
from purchase import enter_virtual_purchase


def import_ecuador_prices(filename):
    return pd.read_excel(filename, sheet_name='Sheet1')


def print_row_ecuador(row):
    print(row['species'], end=' ')
    print(row['Variety'], end=', ')
    if not pd.isnull(row['Comment']):
        print(row['Comment'], end=', ')
    print(row['Grade/cm'], end=', ')
    print(row['St/bx'], end=', ')
    print(row['YYZ(mia)'])


def make_list_from_file(system, filename, po_id):
    variety = ''
    order_date = get_data.get_virtual_purchase_order(po_id)[2]
    week = dates.get_week(order_date)
    year = dates.get_year(order_date)

    df = import_ecuador_prices(filename)
    for index, row in df.iterrows():
        if not pd.isnull(row['$ fob']):
            if row['Variety'].strip() != variety:
                variety = row['Variety'].strip()
                window.drag_window()
                keyboard.write_text(variety)



            print_row_ecuador(row)
            answer = input("next")
            if answer == '':
                try:
                    assortment = add_article()
                except:
                    assortment = lots.get_lot_info_assortment()
                keyboard.f12()
                keyboard.command('down')
                insert_data.insert_virtual_purchase(assortment_code=assortment['assortment_code'], quantity=15,
                                                    packing=row['St/bx'],
                                                    fob="%0.2f" % row['$ fob'], landed="%0.2f" % row['$ fob'],
                                                    virtual_purchase_order_id=po_id, entered=False)
                try:
                    insert_data.insert_weekly_price(system, week, year, assortment['assortment_code'],
                                                    row['selling'])
                except:
                    update_data.update_weekly_price(system, year, week, assortment['assortment_code'],
                                                    row['selling'])

            elif 'q' in answer:
                break
            elif 'n' in answer:
                pass

    return df


def make_list(quantity, packing, price=None, selling=None):
    original_price = price
    items = []
    while True:
        try:
            assortment = add_article()
        except:
            assortment = lots.get_lot_info_assortment()
        if not original_price:
            price = input("FOB price")

        item = {'assortment_code': assortment['assortment_code'], 'quantity': quantity, 'packing': packing,
                'fob': price, 'landed': price, 'assortment': assortment}
        if selling:
            item['selling'] = selling
        items.append(item)
        window.drag_window()
        keyboard.f12()
        choice = input("next")
        if 'n' in choice.lower():
            return items


def calc_landed(price, packing):
    box = 6 * 1.33
    shipping = (box + 9) / packing
    return "%0.2f" % (price * 1.33 + shipping,)


def add_article():
    window.drag_window()
    keyboard.command(('shift', 'F10'))
    assortment = lots.get_lot_info_assortment()
    assortment['system'] = 'f2_canada_real'
    assortment['category_name'] = assortment['catgeory']
    assortment['category_code'] = assortment['category_num']
    del assortment['purchase_date']
    del assortment['lot_number']
    del assortment['supplier_code']
    del assortment['category_num']
    del assortment['landed_price']
    del assortment['catgeory']

    insert_data.insert_assortment(**assortment)
    return assortment


def underline_item(date_str, b):
    w = window.get_window()
    if (date_str in w) == b:
        keyboard.write_text(' ')
    keyboard.command('down')
    return w


def Rosaprima_mday():
    while True:
        try:
            assortment = add_article()
        except:
            assortment = lots.get_lot_info_assortment()
        assortment_code = assortment['assortment_code']
        grade = assortment['grade']
        quantity = 20
        packing = 100
        if str(grade) == '40':
            fob = .69
            p = 125


        elif str(grade) == '50':
            fob = .82
            p = 100

        elif str(grade) == '60':
            fob = .89
            p = 100

        elif str(grade) == '70':
            fob = .92
            p = 75
        elif str(grade) == '80':
            fob = .92
            p = 75
        landed = calc_landed(fob, p)
        virtual_purchase_order_id = 26
        keyboard.f12()
        keyboard.command('down')
        print(assortment)
        input("next")
        time.sleep(.5)
        window.drag_window()
        insert_data.insert_virtual_purchase(assortment_code, quantity, packing, fob, landed, virtual_purchase_order_id,
                                            entered=False)


def easter_list(virtual_purchase_order_id, system, monday_date, quantity, packing):
    year = dates.get_pricing_year(monday_date)
    week = dates.get_pricing_week(monday_date)
    known_prices = dict()
    while True:
        try:
            assortment = add_article()
        except:
            assortment = lots.get_lot_info_assortment()
        if assortment['name'] == '':
            print('Blank')
            print(lots.get_lot_info_assortment())

        assortment_code = assortment['assortment_code']
        grade = assortment['grade']
        fob = input(f"What is the FOB price for {assortment['name']} {grade}")

        if float(fob) in known_prices:
            price = known_prices[float(fob)]
        else:
            price = input(f"What is the Selling price for {assortment['name']} {grade}")
            known_prices[float(fob)] = price

        if not get_data.check_assortment_price(assortment_code, week, year, system):
            insert_data.insert_weekly_price(system, week, year, assortment_code, price)
        else:
            print(price)
            update_data.update_weekly_price(system, year, week, assortment_code, price)

        landed = fob
        time.sleep(.5)
        window.drag_window()
        keyboard.f12()
        keyboard.command('down')
        insert_data.insert_virtual_purchase(assortment_code, quantity, packing, fob, landed, virtual_purchase_order_id,
                                            entered=False)
        input("next")


def set_prices(system, assortment_code, year, start_week, end_week, price):
    for week in range(start_week, end_week):
        if not get_data.check_assortment_price(assortment_code, week, year, system):
            insert_data.insert_weekly_price(system, week, year, assortment_code, price)
        else:

            update_data.update_weekly_price(system, year, week, assortment_code, price)


def add_weekly_items(system, year, startweek, endweek, supplier_code, purchase_day, to_day, offer_end, codes):
    for week in range(startweek, endweek):
        sunday = dates.get_date_sunday(year, week)
        purchase_date = dates.get_date_of_weekday(year, week, purchase_day)
        purchase_date_end = dates.get_date_of_weekday(year, week, to_day)
        offer_start = datetime.datetime.now()
        offer_end_date = dates.get_date_of_weekday(year, week, offer_end['day'])
        offer_end_date = offer_end_date.replace(hour=offer_end['hour'], minute=offer_end['minute'])
        offer_end_date = offer_end_date - datetime.timedelta(weeks=offer_end['advance_weeks'])

        virtual_purchase_order_id = insert_data.insert_virtual_purchase_order(system, supplier_code, purchase_date,
                                                                              purchase_date_end,
                                                                              offer_start,
                                                                              offer_end_date)
        for c in codes:
            if 'selling' not in c:
                print(c)
                c['selling'] = input('selling price?')
            insert_data.insert_virtual_purchase(c['assortment_code'], c['quantity'], c['packing'], c['fob'],
                                                c['landed'], virtual_purchase_order_id,
                                                entered=False)
            if not get_data.check_assortment_price(c['assortment_code'], week, year, system):
                insert_data.insert_weekly_price(system, week, year, c['assortment_code'], c['selling'])
            else:

                update_data.update_weekly_price(system, year, week, c['assortment_code'], c['selling'])
        enter_virtual_purchase(virtual_purchase_order_id)




system = 'f2_canada_real'

# price = input("what is the price")
# #
# try:
#     assortment = add_article()
# except:
#     assortment = lots.get_lot_info_assortment()
#
# for week in range(12,54):
#     update_data.update_weekly_price(system,2020,week, assortment['assortment_code'], price)

# while True:
#     add_article()
#     keyboard.f12()
#     input('next')
#     time.sleep(.1)

filename = r'D:/mday2020/mother2020.xlsx'
a = make_list_from_file(system, filename, 259)
print(a)

# # set_prices(system, assortment_code,year, 10, 54, price)
#
# # for i in range(100):
# #     window_text = underline_item('06-03-20', False)
# #     time.sleep(.1)
#
# startweek = 14
# endweek = 15
#
# supplier_code = 'CAGOLF'
# purchase_day = 'Monday'
# to_day = 'Saturday'
# offer_end = {'day': 'Friday', 'hour': 9, 'minute': 0, 'advance_weeks': 1}
#
# # assortment_code, quantity, packing, fob, landed, virtual_purchase_order_id, entered=False
# # purcases = [
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfaspid', 'quantity': 10, 'packing': 20, 'fob': '1.20', 'landed': '1.20', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #     {'assortment_code': 'cgfleath', 'quantity': 10, 'packing': 20, 'fob': '1.75', 'landed': '1.75', 'entered': False},
# #
# # ]
#
#
# topurchases = [
#     {'assortment_code': 'ealassfa0', 'quantity': 10, 'packing': '100', 'fob': '.3', 'landed': '.3', 'selling': '.89'},
#     {'assortment_code': 'ealasper02', 'quantity': 10, 'packing': '100', 'fob': '.3', 'landed': '.3', 'selling': '1.29'},
#     {'assortment_code': 'cabastHBst', 'quantity': 20, 'packing': '400', 'fob': '.3', 'landed': '.2', 'selling': '.43'},
#     {'assortment_code': 'cabasfHBfy', 'quantity': 20, 'packing': '350', 'fob': '.3', 'landed': '.2', 'selling': '.45'},
#     {'assortment_code': 'missoliw0', 'quantity': 20, 'packing': '12', 'fob': '3.00', 'landed': '.2', 'selling': '8.99'},
# ]
# year = 2020
# add_weekly_items(system, year, startweek, endweek, supplier_code, purchase_day, to_day, offer_end, topurchases,)
#
# # for i in range(20):
# #     print(i, purchases[i])
# #     print()
# # for i in range(20):
# #     input('start')
# #     item = {}
# #     time.sleep(.2)
# #     window.drag_window()
# #     item['assortment_code'] = lots.get_lot_info_assortment()
# #     item['quantity'] = 20
# #     item['packing'] = input('Packing')
# #     item['fob'] = input('fob')
# #     item['landed'] = item['fob']
# #     item['selling'] = input('selling')
# #     purchases.append(item)
#
#
# # easter_list(31, system, datetime.datetime(year=2020, month=4, day=3), quantity, packing)
# # data = []
# # for i in range(26, 28):
# #     data.extend(get_data.get_virtual_purchases_from_order(i))
# #
# # prices = set()
# # for d in data:
# #     print(d)
# #     assortment_code = d[1]
# #     price = d[-3]
# #     prices.add(price)
# #
# # for p in prices:
# #     print(p, float(p) * 1.7)
# #
# # from decimal import Decimal
# #
# # new_prices = {Decimal('1.07'): '1.79', Decimal('0.89'): '1.49', Decimal('1.39'): '2.29', Decimal('0.85'): '1.49',
# #               Decimal('1.35'): '2.29', Decimal('0.92'): '1.59', Decimal('1.38'): '2.39', Decimal('1.45'): '22.49',
# #               Decimal('0.77'): '1.29', Decimal('2.84'): '4.89', Decimal('1.05'): '1.79', Decimal('0.80'): '1.39',
# #               Decimal('1.26'): '2.19', Decimal('0.83'): '1.39', Decimal('1.15'): '1.99', Decimal('1.22'): '2.09',
# #               Decimal('1.29'): '2.19', Decimal('0.86'): '1.49', Decimal('1.18'): '1.99'}
# #
# # for d in data:
# #     price = new_prices[d[-3]]
# #     assortment_code = d[1]
# #     week = 19
# #     year = 2020
# #     if not get_data.check_assortment_price(assortment_code, week, year, system):
# #         insert_data.insert_weekly_price(system, week, year, assortment_code, price)
# #     else:
# #         print(price)
# #         update_data.update_weekly_price(system, year, week, assortment_code, price)
#
#
# # for p in prices:
# #     print (p)
# #     n = input(float(p) * 1.7)
# #     new_prices[p] = n
# #
# # print(new_prices)
#
# # import time
# # window.drag_window()
# # for i in range(20):
# #     keyboard.f11(3)
# # #     keyboard.command('down')
# # #     time.sleep(.01)
# #
# # same  = 0
# # window_text = 'start'
# # while True:
# #     old_text = window_text
# #     window_text = underline_item('28-02-20')
# #     if old_text == window_text:
# #         same += 1
# #     else:
# #         same = 0
# #     if same > 3:
# #         break
# #     time.sleep(.1)
# #
# quantity = 10
# packing = 20
#
# assortment_code = 'hycfancy6w'
# price = 3.2
# year = 2020
#
# print("lisi")
# codes = make_list(quantity, packing)
#
# # easter_list(id, system, datetime.datetime(year=2020, month=4, day=3), quantity, packing)
#
# #
# # offer_end = {'day': 'Wednesday', 'hour': 16, 'minute': 30, 'advance_weeks': 1}
# # add_weekly_items(system, year, 15, 16, 'CAGOLF', 'Monday', 'Saturday', offer_end, codes)
#zmake_list_from_file(system, r'D:/weekly/ecuador_11.xlsx', 261)