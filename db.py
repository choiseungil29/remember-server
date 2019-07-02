import os

from sqlalchemy import create_engine, Column, DateTime, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

url = f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['DB_PORT']}/{os.environ['POSTGRES_DB']}"

engine = create_engine(url, pool_size=50, max_overflow=0)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

class Base:
  id = Column(Integer, primary_key=True)

  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  @property
  def session(self):
    return session.object_session(self)

  def to_json(self):
    data = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.key)
      if type(attr) is datetime:
        attr = int(attr.timestamp() * 1000)
      data[column.key] = attr
    return data

Base = declarative_base(bind=engine, cls=Base)