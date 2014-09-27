# coding=utf-8
from flask import render_template
from app.server import app


@app.route('/')
def index():
    return render_template('index.html')