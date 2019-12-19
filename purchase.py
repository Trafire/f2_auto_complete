from navigation import traverse
from parse import parse, dates
from interface import keyboard
from database import insert_data


def get_input_purchase_lots(system, purchase_date):
    attempts = 0
    lots = {}
    if traverse.main_menu_purchase_default_input_purchases_flowers_date(system, purchase_date):
        while attempts < 5:
            try:
                old_lot_length = len(lots)
                lots.update(parse.get_input_purchase_lots(system, purchase_date))
                new_lot_length = len(lots)
                if old_lot_length == new_lot_length:
                    attempts += 1
                    keyboard.command('pagedown')
                else:
                    attempts = 0

            except:
                attempts += 1
    return lots

def update_purchases(system, purchase_date):
    data = get_input_purchase_lots(system, purchase_date)
    insert_data.insert_purchase_lots(data)
    return True

if __name__ == '__main__':
    system = 'f2_canada_real'
    for d in range(1,31):
        if d > 9:
            purchase_date = f'{d}/12/19'
        else:
            purchase_date = f'0{d}/12/19'
        purchase_date = dates.menu_date(purchase_date)
        #data = parse.get_input_purchase_lots()
        data = get_input_purchase_lots(system, purchase_date)
        insert_data.insert_purchase_lots(data)
