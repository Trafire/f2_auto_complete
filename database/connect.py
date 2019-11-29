
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






'''
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine('postgresql://fmantoine:$pl4nt3n@localhost:3306/crm')
Base = automap_base()
Base.prepare(engine, reflect=True)

Users = Base.classes.f2connection_assortment
session = Session(engine)

res = session.query(Users).first()
print(res.name)


table = 'f2connection_assortment'
session, base, = get_session(table)
res = session.query(base).first()
print(res.name)
help(base)
for b in base:
    print(b)'''