# coding=utf-8

from flask import Flask
from pony.orm import Database

app = Flask(__name__)
app.config.from_pyfile('../default_config.py')
app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

db = Database()
db.bind('postgres', app.config['POSTGRES_CONNECT'])
db.generate_mapping()


@app.before_first_request
def init_db():
    db.disconnect()
