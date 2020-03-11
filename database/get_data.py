from database.connect import c_engine


# def get_purchase_order(system, reference):
#     connection = engine.connect()
#     query = ''' SELECT * from f2connection_virtualpurchaseorder WHERE id=%s'''
#     answer = connection.execute(query, (reference,)).fetchone()

def get_virtual_purchase_order(reference):
    connection = engine.connect()
    query = ''' SELECT * from f2connection_virtualpurchaseorder WHERE id=%s'''
    data =  connection.execute(query, (reference,)).fetchone()
    connection.close()
    return data



def get_time_since_report(system, action, reference):
    connection = engine.connect()
    query = ''' SELECT time_done from f2connection_lastdone
    WHERE system=%s and action=%s and reference=%s
    
    '''
    answer = connection.execute(query, (system, action, reference)).fetchone()
    connection.close()
    if answer:
        return answer[0]
    return False


def get_lot_price(system, lot):
    connection = engine.connect()
    query = f'''SELECT f2connection_weeklyprices.price
                        FROM f2connection_weeklyprices
                    INNER JOIN f2connection_pricedlots on f2connection_pricedlots.price_id = f2connection_weeklyprices.id
                        WHERE lot = '{lot}' and f2connection_pricedlots.system='{system}';
                        '''
    answer = connection.execute(query).fetchone()
    connection.close()
    if answer:
        return answer[0]


def get_lot_price_specials(system, lot):
    connection = engine.connect()
    query = '''SELECT specials.price, prices.price
            FROM f2connection_weeklyspecials as specials
                     RIGHT JOIN
                 f2connection_weeklyprices as prices
                 ON prices.assortment_code = specials.assortment_code
                        AND now() BETWEEN specials.start_time and specials.end_time
                     AND prices.week = specials.week
                     AND prices.year = specials.year
                     AND prices.system = %s
                     RIGHT JOIN f2connection_pricedlots f2cp on prices.id = f2cp.price_id
            WHERE f2cp.lot = %s
            
            '''
    answer = connection.execute(query, (system, lot)).fetchone()
    connection.close()
    if answer:
        for a in answer:
            if a:
                return a


def get_category_name(category_code):
    connection = engine.connect()
    query = f"SELECT category_name FROM f2connection_categories WHERE category_code = '{category_code}'"
    answer = connection.execute(query).fetchone()
    connection.close()

    #    connection.close()
    if answer:
        return answer[0]

def get_virtual_purchases_from_order(order):
    connection = engine.connect()
    query = '''SELECT * from f2connection_virtualpurchases where virtual_purchase_order_id=%s'''
    answer = connection.execute(query, (order,)).fetchall()
    connection.close()
    if answer:
        return answer


"""def get_lot_price(lot, system):
    engine = c_engine()
    connection = engine.connect()
    query = f'''SELECT f2connection_weeklyprices.price
                    FROM f2connection_pricedlots, f2connection_weeklyprices
                    WHERE f2connection_pricedlots.lot = '{lot}' and f2connection_pricedlots.system='{system}'
                    and f2connection_pricedlots.price_id = f2connection_weeklyprices.id
                    ;'''
    answer = connection.execute(query).fetchone()
    if answer:
        return answer[0]
    return None
"""


def check_priced_lots(lot, system):
    connection = engine.connect()
    query = f'''SELECT COUNT(1)
                FROM f2connection_pricedlots
                WHERE lot = '{lot}' and system='{system}';'''
    answer = connection.execute(query).fetchone()
    connection.close()
    return bool(answer[0])

def get_null_recommended(system, lots):
    if not lots:
        return []
    lots = tuple(lots)
    connection = engine.connect()
    if len(lots) > 1:
        query = f'''SELECT lot
                        FROM f2connection_pricedlots
                        WHERE lot IN {lots} and system='{system}' and recommended is null;'''
    else:
        query = f'''SELECT lot
                                FROM f2connection_pricedlots
                                WHERE lot = '{lots[0]}' and system='{system}' and recommended is null;'''

    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:

        result.append(l[0])
    return result


def check_priced_lots_bulk(lots, system):
    lots = tuple(lots)
    connection = engine.connect()
    query = f'''SELECT lot
                FROM f2connection_pricedlots
                WHERE lot IN {lots} and system='{system}';'''
    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:
        result.append(l[0])
    return result


def remove_null_priced_lots_specials(lots, system):
    lots = tuple(lots)
    connection = engine.connect()
    query = f'''SELECT f2cp.lot, specials.price, prices.price
            FROM f2connection_weeklyspecials as specials
                     RIGHT JOIN
                 f2connection_weeklyprices as prices
                 ON prices.assortment_code = specials.assortment_code
                        AND now() BETWEEN specials.start_time and specials.end_time
                     AND prices.week = specials.week
                     AND prices.year = specials.year
                     AND prices.system = '{system}'
                     RIGHT JOIN f2connection_pricedlots f2cp on prices.id = f2cp.price_id
           WHERE f2cp.lot IN {lots} and (specials.price IS NOT NULL or prices.price IS NOT NULL)
                    ;'''
    if len(lots) == 1:
        query = str(query.replace(f'IN {lots}', f"= '{lots[0]}'"))
    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:

        price = l[1]
        if not price:
            price = l[2]
        result.append({'lot': l[0], 'price': str(price)})

    return list(result)


def remove_null_priced_lots(lots, system):
    lots = tuple(lots)
    connection = engine.connect()
    query = f'''SELECT lot, f2connection_weeklyprices.price
                    FROM f2connection_pricedlots
                INNER JOIN f2connection_weeklyprices on f2connection_pricedlots.price_id = f2connection_weeklyprices.id
                    WHERE lot IN {lots} and f2connection_pricedlots.system='{system}' and price IS NOT NULL
                    ;'''
    if len(lots) == 1:
        query = query.replace(f'IN {lots}', f"= '{lots[0]}'")
    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:
        result.append({'lot': l[0], 'price': str(l[1])})

    return list(result)


def check_assortment_price(assortment_code, week, year, system):
    connection = engine.connect()
    assortment_code = assortment_code.replace("'", "''")
    query = f'''SELECT id, price
                    FROM f2connection_weeklyprices
                    WHERE assortment_code = '{assortment_code}' and system='{system}'
                    and week='{week}' and year='{year}' ;'''
    answer = connection.execute(query).fetchone()
    connection.close()
    if answer:
        return answer
    else:
        return False


def get_articles_codes(system):
    connection = engine.connect()
    query = f'''SELECT assortment_code
                FROM f2connection_assortment
                WHERE system='{system}';'''
    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:
        result.append(l[0])
    return result


def get_new_lots(system, lots):
    lots = tuple(lots)
    connection = engine.connect()
    query = f'''SELECT lot
                    FROM f2connection_pricedlots
                    WHERE lot IN {lots} and system='{system}';'''

    if len(lots) == 1:
        query = f'''SELECT lot
                            FROM f2connection_pricedlots
                            WHERE lot = '{lots[0]}' and system='{system}';'''
    answer = connection.execute(query).fetchall()
    connection.close()
    result = []
    for l in answer:
        result.append(l[0])
    return [x for x in lots if x not in result]


def get_purchse_lot(system, lot):
    connection = engine.connect()
    query = f'''SELECT *
                        FROM f2connection_purchases
                        WHERE lot='{lot}' and system='{system}';'''
    answer = connection.execute(query).fetchone()
    connection.close()
    return answer


def get_command(system):
    connection = engine.connect()
    query = f'''SELECT *
                            FROM f2connection_commands
                            WHERE status='unstarted'  and system='{system}';'''
    answer = connection.execute(query).first()
    connection.close()
    if answer:
        return {
            'id': answer[0],
            'command': answer[1],
            'reference': answer[2],
            'status': answer[3],
            'system': answer[4],
        }


def get_input_purchase_date_cmd(id):
    connection = engine.connect()
    query = f'''SELECT purchase_date
                                FROM f2connection_cmdpurchasedates
                                WHERE id={id};'''
    answer = connection.execute(query).first()
    connection.close()
    if answer:
        return answer[0]


def get_purchases_assortment_null(system):
    connection = engine.connect()
    query = f'''
    SELECT lot, purchase_date
        FROM f2connection_purchases
        WHERE system='{system}' and assortment_code isnull;'''
    data = connection.execute(query).fetchall()
    connection.close()
    dlist = []
    for d in data:
        dlist.append((d[0], d[1]))
    return dlist


def get_cmdpurchasedates_id(purchase_date):
    connection = engine.connect()
    query = f'''SELECT id
                                    FROM f2connection_cmdpurchasedates
                                    WHERE purchase_date='{purchase_date}';'''
    answer = connection.execute(query).first()
    connection.close()
    if answer:
        return answer[0]


def get_stock_purchase_date(lot):
    connection = engine.connect()
    query = f'''SELECT id
                                        FROM f2connection_cmdpurchasedates
                                        WHERE purchase_date='{purchase_date}';'''





engine = c_engine()


if '__main__' == __name__:
    system = 'f2_canada_real'
    # print(get_lot_price('640619', 'f2_canada_real'))
    year = 2019
    week = 49
    lots = ['645465',
            '645789',
            '649245',
            '649245',
            '648696',
            '648004']
    #print(remove_null_priced_lots_specials(lots, system))
    # print(get_purchases_assortment_null(system))
    # lots = ['639690', '641538', '640571']
    # print(check_priced_lots_bulk(lots, system))
    # print(get_articles_codes(system))



