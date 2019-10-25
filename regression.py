from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


dbfile = 'matchmaker.sqlite3'

engine = create_engine(f'sqlite:///db/{dbfile}')
Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
