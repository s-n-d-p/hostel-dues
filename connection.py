from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DuesRecord

engine = create_engine('sqlite:///dues_record.db',connect_args = {'check_same_thread':False})
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
# hacktoberfest
