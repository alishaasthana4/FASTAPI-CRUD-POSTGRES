from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
DB_URL='postgresql://postgres:ali123@localhost/CRUD'
engine=create_engine(DB_URL)
sessionlocal=sessionmaker(bind=engine)
Base=declarative_base()

