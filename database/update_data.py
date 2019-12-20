from database.connect import c_engine


def update_landed(lot, system, landed):
    engine = c_engine()
    connection = engine.connect()
    query = f'''
    UPDATE f2connection_pricedlots
        SET landed = {landed}
        WHERE lot='{lot}' and system = '{system}';
    '''
    connection.execute(query)
    connection.close()


def update_command_status(id, status):
    engine = c_engine()
    connection = engine.connect()
    query = f'''
        UPDATE f2connection_commands
            SET status = '{status}'
            WHERE id={id};'''

    connection.execute(query)
    connection.close()




def update_unmatched_purchases():
    engine = c_engine()
    connection = engine.connect()
    query = f'''
        UPDATE f2connection_purchases
            SET assortment_code = f2connection_weeklyprices.assortment_code
            FROM f2connection_weeklyprices, f2connection_pricedlots
            WHERE f2connection_purchases.lot=f2connection_pricedlots.lot and f2connection_purchases.system = f2connection_pricedlots.system and f2connection_pricedlots.price_id= f2connection_weeklyprices.id;
        '''
    connection.execute(query)
    connection.close()


def update_purchases_assortment(system, lot, assortment_code):
    engine = c_engine()
    connection = engine.connect()
    query = f'''
            UPDATE f2connection_purchases
                SET assortment_code = '{assortment_code}'
                WHERE lot='{lot}' and system='{system}';'''
    print(query)
    connection.execute(query)
    connection.close()

