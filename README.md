### Uses: Python3.7, Flask, SQLAlchemy, Alembic, Docker, Postgresql

## 환경 설정
1. virtualenv 환경 설정 (virtualenv venv --python=python3.7)
2. venv 상태로 전환 (venv/bin/activate)
3. pip install -r requirements.txt
4. docker-compose up -d local_db
5. alembic 셋팅 ./scripts/alembic.sh upgrade head
6. db 초기화 python ./scripts/init.py
7. 서버 실행 ./scripts/local_server.sh

## 개선 가능한 사항
 - API Exception 별도로 생성하여 status code와 msg를 함께 함께 내려주도록 할 수 있음
