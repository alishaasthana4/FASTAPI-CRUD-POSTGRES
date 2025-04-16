from sqlalchemy import Column, Integer, String
from database import Base

class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password=Column(String)
    api_key=Column(String,unique=True,nullable=False)




