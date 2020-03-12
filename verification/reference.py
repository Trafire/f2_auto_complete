import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)).strip(r'verification')

VERIFICATION = {}

VERIFICATION['login'] = {
    # images
    'image_screen_open': os.path.join(PACKAGE_DIRECTORY, r'images/verification/login/login_screen_open.PNG'),
    'image_cancel_button': os.path.join(PACKAGE_DIRECTORY, r'images/verification/login/login_screen_cancel_button.PNG'),
    'image_ok_button': os.path.join(PACKAGE_DIRECTORY, r'images/verification/login/login_screen_cancel_button.PNG'),
    'image_annulern_button': os.path.join(PACKAGE_DIRECTORY,
                                          r'images/verification/login/login_screen_annulern_button.PNG'),
    'list_str_screen_titles_ok': [
        'Select Private Key File For Authentication',
        'Afsluiten'
    ],

    'list_str_screen_titles_cancel': [
        'Select Private Key File For Authentication',
    ],
    'list_str_screen_titles_annulern': [
        'Loginnaam of wachtwoord verkeerd ingevoerd',
        ' Connect  login',
        'Select Private Key File For Authentication',
        'Inloggen nieuwe sessie',
    ],
}

VERIFICATION['f2_window'] = {
    'any': '(© Uniware Computer Systems BV)',
    'login': ' Connect  login',
}

VERIFICATION['system_options'] = {
    'f2_canada_menu_number': '07',
    'f2_canada_real_system_number': '1',
    'f2_canada_test_system_number': '3',

}

VERIFICATION['system'] = {
    'f2_canada_test': [{'target': 'Toronto (TEST)', 'location': (1, 92)}],
    'f2_canada_real': [{'target': 'FleuraMetz Toronto', 'location': (1, 92)}],
}

VERIFICATION['screens'] = {
    'text_login_menu_1': ['01)   FleuraMetz Holland', 'FleuraMetz Toronto'],

    'text_login_menu_2_large': [{'target': '║       1)   Toronto                    ║',
                                 'location': (5, 18)},
                                {'target': '© Uniware Computer Systems BV', 'location': (1, 24)}],
    'text_login_menu_2': ['║       1)   Toronto                    ║', '║       3)   Toronto Testsysteem        ║'],
    'main_menu': [{'target': 'Main Menu', 'location': (2, 92)},
                  {'target': 'Orders', 'location': (5, 4)},
                  {'target': '© Uniware Computer Systems BV',
                   'location': (1, 3)}],
    'main_menu-maintenance_data': [{'target': 'Data maintenance', 'location': (2, 92)},
                                   {'target': 'Orders', 'location': (5, 4)},
                                   {'target': 'Relations', 'location': (5, 29)},
                                   {'target': '© Uniware Computer Systems BV', 'location': (1, 3)}],
    'main_menu-maintenance_data-pricelists': [{'target': 'Orders', 'location': (5, 4)},
                                              {'target': 'Relations', 'location': (5, 29)},
                                              {'target': '© Uniware Computer Systems BV', 'location': (1, 3)},
                                              {'target': 'Pricelist type', 'location': (5, 53)},
                                              {'target': 'Pricelists', 'location': (2, 92)},
                                              {'target': 'Pricelists', 'location': (9, 29)}],
    'main_menu-maintenance_data-pricelists-edit_pricelist': [{'target': 'Edit pricelist', 'location': (2, 92)},
                                                             {'target': '║Flowers             ║', 'location': (4, 54)},
                                                             {'target': '© Uniware Computer Systems BV',
                                                              'location': (1, 3)}],
    'main_menu-maintenance_data-pricelists-edit_pricelist-flowers': [
        {'target': 'Edit pricelist Flowers', 'location': (2, 92)},
        {'target': '© Uniware Computer Systems BV', 'location': (1, 3)}],

    'main_menu-maintenance_data-pricelists-edit_pricelist-flowers-select': [
        {'target': 'Edit pricelist Flowers', 'location': (2, 92)},
        {'target': '{pricelist}', 'location': (4, 2)},
        {'target': '© Uniware Computer Systems BV', 'location': (1, 3)},
    ],
    'main_menu-stock': [{'target': 'Stock (actual)', 'location': (5, 29)},
                        {'target': 'Edit stock', 'location': (5, 54)}],

    'main_menu-stock-virtual-stock-location': [{'target': 'Stock (actual)', 'location': (5, 29)},
                                               {'target': 'Edit stock', 'location': (5, 54)}],
    'main_menu-stock-virtual-stock-location-edit_stock': [{'target': 'Edit stock', 'location': (2, 92)},
                                                          {'target': 'Til:', 'location': (4, 18)}],
    "main_menu-stock-stock_per_location": [{'target': '   Stock location  ', 'location': (2, 89)},
                                           {'target': 'Edit stock per group', 'location': (6, 54)}],
    "main_menu-stock-stock_per_location-edit_stock": [{'target': 'Edit stock', 'location': (2, 92)},
                                                      {'target': 'Til:', 'location': (4, 18)}],
    "main_menu-stock-stock_per_location-edit_stock-date": [{'target': 'Edit stock', 'location': (2, 92)},
                                                           {'target': 'Fro: {from_date}', 'location': (4, 2)},
                                                           {'target': 'Til: {to_date}', 'location': (4, 18)}],
    "main_menu-stock-stock_per_location-edit_stock-date-flowers": [
        {'target': 'Edit stock Flowers', 'location': (2, 92)}, {'target': 'Locat', 'location': (5, 53)},
        {'target': 'Omschrijving', 'location': (5, 65)}],
    "stock_per_location-flowers-location": [{'target': 'Edit stock Flowers', 'location': (2, 92)},
                                            {'target': 'Location: {location}', 'location': (33, 41)},
                                            {'target': 'Description', 'location': (5, 15)}],
    'virtual_stock_per_location-flowers-location': [{'target': 'Edit stock Flowers', 'location': (2, 92)},
                                                    {'target': 'Description', 'location': (5, 16)},
                                                    {'target': 'Pack.:', 'location': (33, 69)}],
    "stock_per_location-flowers-location-price_level": [{'target': 'Pricegroup:    {level}', 'location': (4, 59)}],
    "lot_info": [{'target': 'Intern partijnummer  : {lot_number}', 'location': (18, 97)}],
    "virtual_lot_info": [{'target': 'Intern partijnummer  : {lot_number}', 'location': (17, 97)}],

    'main_menu-purchase': [{'target': 'Purchase', 'location': (2, 92)}, {'target': 'Purchase', 'location': (5, 55)},
                           {'target': 'Purchase', 'location': (6, 4)}, {'target': 'Purchase', 'location': (7, 29)},
                           {'target': 'Purchase', 'location': (8, 55)}, {'target': 'Purchase', 'location': (9, 29)},
                           {'target': 'Purchase', 'location': (11, 55)},
                           {'target': 'Purchase/distribute', 'location': (5, 55)}],
    'main_menu-purchase-default': [{'target': 'Purchase', 'location': (2, 92)},
                                   {'target': 'Purchase', 'location': (5, 55)},
                                   {'target': 'Purchase', 'location': (6, 4)},
                                   {'target': 'Purchase', 'location': (7, 29)},
                                   {'target': 'Purchase', 'location': (8, 55)},
                                   {'target': 'Purchase', 'location': (9, 29)},
                                   {'target': 'Purchase', 'location': (11, 55)},
                                   {'target': 'Purchase/distribute', 'location': (5, 55)}],
    'main_menu-purchase-default-purchase_distribute': [{'target': 'Purchase', 'location': (2, 92)},
                                                       {'target': 'Purchase', 'location': (5, 55)},
                                                       {'target': 'Purchase', 'location': (6, 4)},
                                                       {'target': 'Purchase', 'location': (7, 29)},
                                                       {'target': 'Purchase', 'location': (8, 55)},
                                                       {'target': 'Purchase', 'location': (9, 29)},
                                                       {'target': 'Purchase', 'location': (11, 55)},
                                                       {'target': 'Purchase/distribute', 'location': (5, 55)}],
    'main_menu-purchase-default-purchase_distribute_flowers': [
        {'target': '║Flowers             ║', 'location': (4, 54)},
        {'target': 'Purchase/distribute', 'location': (2, 92)}],
    'main_menu-purchase-default_insert_virtual_purchase': [{'target': 'Purchase', 'location': (2, 92)},
                                                           {'target': 'Purchase', 'location': (5, 55)},
                                                           {'target': 'Purchase', 'location': (6, 4)},
                                                           {'target': 'Purchase', 'location': (7, 29)},
                                                           {'target': 'Purchase', 'location': (8, 55)},
                                                           {'target': 'Purchase', 'location': (9, 29)},
                                                           {'target': 'Purchase', 'location': (11, 55)},
                                                           {'target': 'Purchase/distribute', 'location': (5, 55)}],
    'main_menu-purchase-default_insert_virtual_purchase_flowers': [
        #{'target': '║Flowers             ║', 'location': (4, 54)},
        {'target': 'Insert virtual purchases', 'location': (2, 92)}],
    'main_menu-purchase-default-input_purchases': [{'target': '║Flowers             ║', 'location': (4, 54)},
                                                   {'target': 'Input purchases', 'location': (2, 92)}],
    'main_menu-purchase-default-input_purchases-flowers':
        [{'target': 'Date    :', 'location': (4, 2)}, {'target': 'Input purchases', 'location': (2, 92)}],

}
VERIFICATION['navigation'] = {
    'main_menu-maintenance_data': 'Maintenance data',
    'main_menu-maintenance_data-pricelists': 'Pricelists',
    'main_menu-maintenance_data-pricelists-edit_pricelist': 'Edit pricelist',
    'main_menu-maintenance_data-pricelists-edit_pricelist-flowers': 'Flowers',
    'main_menu-stock': 'Stock',
    'main_menu-stock-stock_per_location': 'Stock per location',
    'main_menu-stock-stock_per_location-edit_stock': '{HOME}',
    "main_menu-stock-stock_per_location-edit_stock-date-flowers": '{HOME}',
    'main_menu-purchase': "Purchase",
    'main_menu-purchase-default': '{HOME}{ENTER}',
    'main_menu-purchase-default-purchase_distribute': '{HOME}{ENTER}',
    'main_menu-purchase-default-purchase_distribute_flowers': '',
    'main_menu-purchase-default_insert_virtual_purchase': 'Insert virtual',
    'main_menu-purchase-default_insert_virtual_purchase_flowers': '',
    'main_menu-purchase-default-input_purchases': 'Input purchases',
    'main_menu-purchase-default-input_purchases-flowers': '{HOME}{ENTER}',
    'main_menu-stock-virtual-stock-location': 'Virtual stock location',
    'main_menu-stock-virtual-stock-location-edit_stock': '{HOME}{ENTER}',
}

VERIFICATION['price_list'] = {
    '002': {
        'name': 'Cooler',
    },
    '003': {
        'name': 'Shipment',
    },
    '006': {
        'name': 'Additions',
    },
    '011': {
        'name': 'Universe',
    },
    '031': {
        'name': 'Pre-booking Holland',
    },
    '050': {
        'name': 'To Price',
    },
    '051': {
        'name': 'Direct',
    },
    '052': {
        'name': 'New Zealand',
    },
    '053': {
        'name': 'Available',
    },
    '054': {
        'name': 'Box Program',
    },
    '061': {
        'name': 'Box Program',
    },
    '062': {
        'name': 'VDAY',
    },
}
VERIFICATION['pricing'] = {
    'f8-pricing': [{'target': 'Edit pricelist Flowers', 'location': (2, 92)},
                   {'target': 'Articlegroup', 'location': (4, 23)},
                   {'target': 'Val', 'location': (11, 60)}, {'target': 'Perc.', 'location': (11, 65)}],
    'in_group-pricing': [{'target': 'Edit pricelist Flowers', 'location': (2, 92)},
                         {'target': 'Articlegroup', 'location': (4, 23)},
                         ],

}
