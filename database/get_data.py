from database.connect import c_engine



def get_time_since_report(system, action, reference):
    connection = engine.connect()
    query = ''' SELECT time_done from f2connection_lastdone
    WHERE system=%s and action=%s and reference=%s
    
    '''
    answer = connection.execute(query, (system, action, reference)).fetchone()
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
    if answer:
        return answer[0]


def get_category_name(category_code):

    connection = engine.connect()
    query = f"SELECT category_name FROM f2connection_categories WHERE category_code = '{category_code}'"
    answer = connection.execute(query).fetchone()

    #    connection.close()
    if answer:
        return answer[0]


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
    return bool(answer[0])


def check_priced_lots_bulk(lots, system):
    lots = tuple(lots)
    connection = engine.connect()
    query = f'''SELECT lot
                FROM f2connection_pricedlots
                WHERE lot IN {lots} and system='{system}';'''
    answer = connection.execute(query).fetchall()
    result = []
    for l in answer:
        result.append(l[0])
    return result


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
    return answer


def get_command(system):
    connection = engine.connect()
    query = f'''SELECT *
                            FROM f2connection_commands
                            WHERE status='unstarted'  and system='{system}';'''
    answer = connection.execute(query).first()
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
    if answer:
        return answer[0]


def get_purchases_assortment_null(system):
    connection = engine.connect()
    query = f'''
    SELECT lot, purchase_date
        FROM f2connection_purchases
        WHERE system='{system}' and assortment_code isnull;'''
    data = connection.execute(query).fetchall()
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
    if answer:
        return answer[0]

engine = c_engine()


if '__main__' == __name__:
    system = 'f2_canada_real'
    # print(get_lot_price('640619', 'f2_canada_real'))
    year = 2019
    week = 49
    # print(get_purchases_assortment_null(system))
    print(get_cmdpurchasedates_id('2019-12-27'))
    print(get_cmdpurchasedates_id('2019-5-27'))
    print(get_cmdpurchasedates_id('2019-11-27'))

    # print(check_assortment_price('calsurpE0p', week, year, system))

    # lots = ['639690', '641538', '640571']
    # print(check_priced_lots_bulk(lots, system))
    # print(get_articles_codes(system))
