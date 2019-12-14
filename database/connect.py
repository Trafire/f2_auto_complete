
from auth.passwords import cloud_db
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


def c_engine():
    username = cloud_db['username']
    password = cloud_db['password']
    engine = create_engine(f'postgresql://{username}:{password}@localhost:3306/crm')
    return engine



def get_session():
    '''engine = c_engine()
    metadata = MetaData(engine)
    class_table = Table(table, metadata, autoload=True)
    mapper(classtype, class_table)
    Session = sessionmaker(bind=engine)
    session = Session()'''
    engine = c_engine()
    #base = get_base_class(engine, table)
    session = Session(engine)

    return session

def get_base_class(engine, table):
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    return Base.classes[table]


