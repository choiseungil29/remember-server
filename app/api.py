import json

from flask import Blueprint, request, session
from decorator import router

from app import models

import db


blueprint_api = Blueprint('api', __name__, url_prefix='/api')

api = router(blueprint_api)


# TODO
# login 구현
# logout 구현
# access_level 구현


@api('/')
def index(context):
  return 'hi'

@api('/login', methods=['POST'])
def login(context):
  """
  유저 로그인 API
  requests:
   - login_id: str
   - login_password: str
  """

  data = request.json

  if 'uid' in session and context.user and context.user.id == session['uid']:
    return json.dumps(context.user.to_json())
  
  user = db.session.query(models.User).\
    filter(models.User.login_id == data['login_id']).\
    filter(models.User.login_password == data['login_password']).\
    first()
  
  if not user:
    return json.dumps({'result': '아이디 또는 패스워드 오류입니다.'})
  
  session['uid'] = user.id

  return json.dumps(user.to_json())

@api('/logout', methods=['POST'])
def logout(context):
  """
  유저 로그아웃 API
  """

  if 'uid' not in session:
    raise Exception('로그인이 되어있지 않습니다.')

  del session['uid']
  return json.dumps({'result': '로그아웃 되었습니다.'})

@api('/users', methods=['GET'], access_level=1)
def users(context):
  """
  유저 전체 정보 조회 API
  Master 등급과 Diamond등급만 조회 가능
  """
  
  users = db.session.query(models.User).\
    all()

  if context.user.priority == 1:
    users = list(filter(lambda x: x.priority > 1, users))

  return json.dumps([u.to_json() for u in users])

@api('/users/create', methods=['POST'])
def user_create(context):
  """
  유저 생성 API

  requests:
   - login_id: str
   - login_password: str
   - priority: int
   - name: str
  """

  req = request.json

  if 'name' not in req:
    raise
  if 'login_id' not in req:
    raise
  if 'login_password' not in req:
    raise
  if 'priority' not in req:
    raise

  if req['priority'] <= context.user.priority:
    raise Exception('생성할 수 없는 level입니다')

  if req['priority'] >= len(models.User.levels()) / 2:
    raise Exception('범위 바깥에 있는 level입니다.')

  if db.session.query(models.User).\
    filter(models.User.login_id == req['login_id']).\
    first():
    raise Exception('이미 존재하는 ID입니다.')
  
    
  user = models.User()
  user.name = req['name']
  user.login_id = req['login_id']
  user.login_password = req['login_password']
  user.priority = req['priority']

  db.session.add(user)
  db.session.commit()

  return json.dumps(user.to_json())

@api('/users/<int:id>/remove', methods=['POST'], access_level=1)
def user_remove(context, id):
  """
  유저 삭제 API
  """

  user = db.session.query(models.User).\
    filter(models.User.id == id).\
    filter(models.User.priority > context.user.priority).\
    first()

  if not user:
    raise Exception('존재하지 않는 유저입니다.')

  db.session.delete(user)
  db.session.commit()

  return json.dumps(user.to_json())

@api('/users/<int:id>/update', methods=['POST'], access_level=1)
def user_update(context, id):
  """
  유저 업데이트 API

  requests:
   - login_id: str
   - login_password: str
   - priority: int
   - name: str
  """

  req = request.json

  user = db.session.query(models.User).\
    filter(models.User.id == id).\
    first()
  
  if not user:
    raise Exception('이미 존재하는 ID입니다.')
  
  if context.user.priority == 1 and user.priority <= 1:
    raise Exception('수정할 수 없는 TARGET USER입니다.')

  user.login_id = req['login_id']
  user.login_password = req['login_password']
  user.priority = req['priority']
  user.name = req['name']

  db.session.commit()

  return json.dumps(user.to_json())

@api('/users/<int:id>', methods=['GET'])
def user_info(context, id):
  """
  예외
   - access_level은 1이하만 가능 + 동급 레벨 이전까지만 조회 가능
  """

  user = db.session.query(models.User).\
    filter(User.id == id).\
    filter(User.priority > context.user.priority).\
    first() 
  
  if not user and id == context.user.id:
    return ujson.dumps(user.to_json())
  
  if user is None:
    return 'error'

  return ujson.dumps(user.to_json())