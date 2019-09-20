from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:passwd@127.0.0.1:3306/habitpro')#127.0.0.1==localhost,注意修改数据库密码passwd
DbSession = sessionmaker(bind = engine)

Base = declarative_base()

