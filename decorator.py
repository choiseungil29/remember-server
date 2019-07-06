import hashlib
import random
import string

from flask import session

from functools import wraps

import db

from app import models


def router(application, **kwargs):
  def route(uri, access_level=None, **kwargs):
    def wrapper(fn):
      @wraps(fn)
      def decorator(*args, **kwargs):
        context = ApiContext()
        if 'uid' in session:
          user = db.session.query(models.User).\
            filter(models.User.id == session['uid']).\
            first()
          context.user = user
        
        kwargs['context'] = context
        if context.access(access_level):
          res = fn(*args, **kwargs)
        else:
          raise "접근 권한이 없습니다."
        return res
      
      application.add_url_rule(uri, fn.__name__, decorator, **kwargs)
      return decorator

    return wrapper
  return route


class ApiContext:
  def __init__(self):
    self.user = None
  
  def access(self, access_level):
    if access_level is None:
      return True
    
    if access_level is not None and self.user is None:
      return False
    
    if access_level >= self.user.priority:
      return True
    return False