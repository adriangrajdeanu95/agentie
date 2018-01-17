import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='postgresql://useragentie:pass@localhost:5432/agentie',
    SECRET_KEY='development-key',
    USERNAME='useragentie',
    PASSWORD='pass',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))
db.init_app(app)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello/')
def hello():
    return 'Hello, World'


@app.route('/login/')
def login():
    return 'login page'


@app.route('/register/')
def register():
    return 'register page'


@app.route('/search/')
def search():
    return 'search page'


@app.route('/trip/<int:trip_id>/')
def trip(trip_id):
    return 'trip no. %d' % trip_id


@app.route('/me/')
def me():
    return 'my page'


@app.route('/admin/')
def admin():
    return 'admin page'
