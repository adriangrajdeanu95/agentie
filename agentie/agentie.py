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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
        conn = engine.connect()
        stmt = text('SELECT * FROM "Orase"')
        result = conn.execute(stmt)
        cities = result.fetchall()
        print(cities[0][1])
        return render_template('index.html', cities=cities)
    if request.method == 'POST':
        return redirect(url_for('.search', city=request.form['selected_city'],\
                                stars=request.form['selected_stars'], \
                                price=request.form['selected_price']))


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


@app.route('/search/<city>/<stars>/<price>/')
def search(city, stars, price):
    engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
    conn = engine.connect()
    stmt = text('SELECT "Excursie"."ID_Excursie", "Excursie"."Pret", "Excursie"."Data_Inceput_Perioada", \
		        "Excursie"."Nr_zile", "Cazare"."Nume", "Cazare"."Descriere", "Cazare"."All_inclusive" \
                FROM "Excursie" \
                INNER JOIN "Excursie_Cazare" ON "Excursie"."ID_Excursie"="Excursie_Cazare"."ID_Excursie"\
                INNER JOIN "Cazare" ON "Excursie_Cazare"."ID_Cazare"="Cazare"."ID_Cazare"\
                INNER JOIN "Orase" ON "Cazare"."ID_Oras"="Orase"."ID_Oras"\
                WHERE "Orase"."Nume"=\''+str(city)+'\' AND "Cazare"."Nr_Stele"='+str(stars)+' \
                AND "Excursie"."Pret"<'+str(price)+'\
                ORDER BY "Excursie"."Data_Inceput_Perioada"')
    result = conn.execute(stmt)
    trips = result.fetchall()
    return render_template('search.html', trip=trips, city=city, stars=stars)


@app.route('/trip/<int:trip_id>/', methods=['GET', 'POST'])
def trip(trip_id):
    if request.method == 'GET':
        engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
        conn = engine.connect()
        stmt = text('SELECT * FROM "Excursie" \
                INNER JOIN "Excursie_Cazare" ON "Excursie"."ID_Excursie"="Excursie_Cazare"."ID_Excursie" \
                INNER JOIN "Cazare" ON "Excursie_Cazare"."ID_Cazare"="Cazare"."ID_Cazare" \
                INNER JOIN "Orase" ON "Cazare"."ID_Oras"="Orase"."ID_Oras" \
                WHERE "Excursie"."ID_Excursie"='+str(trip_id))
        result = conn.execute(stmt)
        trip_details = result.fetchone()
        print(trip_details)
        stmt = text('SELECT * FROM "Excursie" \
                    INNER JOIN "Excursie_Transport" ON "Excursie"."ID_Excursie"="Excursie_Transport"."ID_Excursie" \
                    INNER JOIN "Transport" ON "Excursie_Transport"."ID_Transport"="Transport"."ID_Transport" \
                    INNER JOIN "Comp_Transport" ON "Transport"."ID_Comp_transport"="Comp_Transport"."ID_Comp_Transport" \
                    WHERE "Excursie"."ID_Excursie"=' + str(trip_id))
        result = conn.execute(stmt)
        transport_details = result.fetchone()

        stmt = text('SELECT * FROM "Orase"')
        result = conn.execute(stmt)
        cities = result.fetchall()

        return render_template('trip.html', trip=trip_details, transp=transport_details, cities=cities)
    if request.method == 'POST':
        engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
        conn = engine.connect()
        stmt = text('SELECT "ID_Oras" FROM "Orase" \
                        WHERE "Orase"."Nume"=\'' + str(request.form['selected_city']) + '\'')
        result = conn.execute(stmt)
        city_id = result.fetchone()
        stmt = text('INSERT INTO "Client" ("Nume", "Oras_Domiciliu", "CNP", "Observatii", "Asig_Sanatate", "Nr_Telefon", "Email") \
                        VALUES (\''+str(request.form['name'])+'\', \
                        \''+str(city_id[0])+'\', \
                        \''+str(request.form['cnp'])+'\', \' \', \
                        \''+str(request.form['asig-sanatate'])+'\', \
                        \''+str(request.form['telefon'])+'\', \
                        \''+str(request.form['email'])+'\')')
        result = conn.execute(stmt)
        return redirect(url_for('trip', trip_id=trip_id))


@app.route('/admin/', methods=['GET', 'DELETE'])
def admin():
    if session.get('logged-in') == True:
        if request.method == 'GET':
            engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
            conn = engine.connect()
            stmt = text('SELECT * FROM "Orase" ORDER BY "Nume"')
            result = conn.execute(stmt)
            cities = result.fetchall()
            return render_template('admin.html', cities=cities)
        return 'admin page'
    return(redirect(url_for('login')))

@app.route('/delete/city/<int:id>', methods=['POST'])
def delete_city(id):
    if session.get('logged-in') == True:
        engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
        conn = engine.connect()
        stmt = text('DELETE FROM "Orase" WHERE "ID_Oras='+str(id))
        conn.execute(stmt)
    return(redirect(url_for('admin')))

@app.route('/edit/city/<int:id>', methods=['GET', 'POST'])
def edit_city(id):
    if session.get('logged-in') == True:
        if request.method == 'GET':
            engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
            conn = engine.connect()
            stmt = text('SELECT * FROM "Orase" WHERE "ID_Oras"='+str(id))
            result = conn.execute(stmt)
            city = result.fetchone()
            return render_template('edit-city.html', city=city)
        if request.method == 'POST':
            engine = create_engine('postgresql://useragentie:pass@localhost:5432/agentie')
            conn = engine.connect()
            if request.form['name']:
                stmt = text('UPDATE "Orase" SET "Nume"=\''+str(request.form['name'])+'\' WHERE "ID_Oras"=' + str(id))
                conn.execute(stmt)
            if request.form['country']:
                stmt = text('UPDATE "Orase" SET "Tara"=\''+str(request.form['country'])+'\' WHERE "ID_Oras"=' + str(id))
                conn.execute(stmt)
            if request.form['name']:
                stmt = text('UPDATE "Orase" SET "Rating"='+str(request.form['rating'])+' WHERE "ID_Oras"=' + str(id))
                conn.execute(stmt)
            print(request.form['name'])
    return(redirect(url_for('admin')))