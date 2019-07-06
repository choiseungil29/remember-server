from sqlalchemy import create_engine, Column, DateTime, Integer, String

from db import Base


# 유저 구현을 해야한다.
# 유저는 Level을 갖는다
# 유저의 Level은 그 자체로 객체다.
# 1:1관계다.
class User(Base):
  __tablename__ = 'users'

  priority = Column(Integer)

  name = Column(String)
  login_id = Column(String, unique=True)
  login_password = Column(String)

  def __init__(self):
    Base.__init__(self)
  
  @staticmethod
  def levels():
    data = {
      0: 'master',
      1: 'diamond',
      2: 'platinum',
      3: 'gold',
      4: 'silver',
      5: 'bronze'
    }

    data.update(dict((v, k) for k, v in data.items()))
    return data

  @property
  def level(self):
    return User.levels()[self.priority]
  
  def to_json(self):
    res = Base.to_json(self)
    res['level'] = self.level
    return res
