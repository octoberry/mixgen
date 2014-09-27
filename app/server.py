# coding=utf-8

from flask import Flask
from pony.orm import Database

app = Flask(__name__)
app.config.from_pyfile('../default_config.py')
app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

db = Database()


# @app.before_first_request
# def init_db():
#     if db.provider is None:
#         db.bind('postgres', app.config['DATABASE'])
#     if db.schema is None:
#         db.generate_mapping()
#     db.disconnect()
