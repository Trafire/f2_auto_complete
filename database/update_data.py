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


