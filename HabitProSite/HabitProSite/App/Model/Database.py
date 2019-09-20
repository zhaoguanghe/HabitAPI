from sqlalchemy import Column,Integer,String,DateTime
from Base import Base

class Sign(Base):
    __tablename__ = 't_sign'
    Id = Column(Integer, primary_key = True, autoincrement=True)
    UserId = Column(String(50))
    Date = Column(String(20))

class Token(Base):
    __tablename__ = 't_token'
    Id = Column(Integer, primary_key = True)
    Access_token = Column(String(200))
    Time = DateTime()

class Form(Base):
    __tablename__ = 't_formid'
    Id = Column(Integer, primary_key = True, autoincrement=True)
    UserId = Column(String(50))
    FormId = Column(String(20))
    Date = Column(String(50))

class Habit(Base):
    __tablename__ = 't_habit'
    Id = Column(Integer, primary_key = True, autoincrement=True)
    UserId = Column(String(50))
    Hname = Column(String(30))
    Htime = Column(String(10))
    Hrange = Column(String(10))
    Hword = Column(String(50))
    Hcheck = Column(String(5))
    Date = Column(String(20))
    Status = Column(Integer)