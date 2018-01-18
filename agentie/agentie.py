import os, hashlib
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy
from models import *
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='postgresql://useragentie:pass@localhost:5432/agentie',
    SECRET_KEY='dtqf46vsa!803gon_5w!nm4_&&oo2+#19t=9b$%-$^r_s5+pzx*',
    USERNAME='useragentie',
    PASSWORD='pass',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))
app.secret_key='dtqf46vsa!803gon_5w!nm4_&&oo2+#19t=9b$%-$^r_s5+pzx*'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
        conn = engine.connect()
        stmt = text('SELECT * FROM "Admin"')
        result = conn.execute(stmt)
        row = result.fetchone()
        hash_object = hashlib.sha256(request.form['password'])
        hex_dig = hash_object.hexdigest()
        if request.form['username'] == row[1].encode('utf-8') and hex_dig == row[2].encode('utf-8'):
            conn.close()
            session['logged-in'] = True
            return redirect(url_for('admin'))
        conn.close()
    return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('logged-in', None)
    return redirect(url_for('login'))


@app.route('/administrator/')
def administrator():
    return 'admin page'


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
