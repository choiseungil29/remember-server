
#! venv/bin/python

import os
import sys

import dotenv

import json

dotenv.load_dotenv('local.env')
sys.path.append(os.getcwd())

os.environ['POSTGRES_HOST'] = 'localhost'

import db
from app import models

admin = db.session.query(models.User).\
  filter(models.User.priority == 0).\
  first()

if not admin:
  admin = models.User()
  admin.name = 'admin'
  admin.login_id = 'admin'
  admin.login_password = 'admin'
  admin.priority = 0
  db.session.add(admin)
  db.session.commit()
