from flask import Blueprint, request
from decorator import router


blueprint_api = Blueprint('api', __name__, url_prefix='/api')

api = router(blueprint_api)


@api('/')
def index(context):
  return 'hi'
