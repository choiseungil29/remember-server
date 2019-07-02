import hashlib
import random
import string

from flask import session

from functools import wraps

import cProfile
pr = cProfile.Profile()

def router(application, **kwargs):
  def route(uri, **kwargs):
    def wrapper(fn):
      @wraps(fn)
      def decorator(*args, **kwargs):
        pr.enable()
        context = ApiContext()
        kwargs['context'] = context
        res = fn(*args, **kwargs)
        pr.disable()
        return res
      application.add_url_rule(uri, fn.__name__, decorator, **kwargs)
      return decorator

    return wrapper
  return route


class ApiContext:
  def __init__(self):
    pass