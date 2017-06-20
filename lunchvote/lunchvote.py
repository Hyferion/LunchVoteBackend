import os
import sqlite3
import json
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , lunchvote.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lunchvote.db'),
    SECRET_KEY='456213546312adfadsf87aksdfaskj',
    USERNAME='admin',
    PASSWORD=''
))
app.config.from_envvar('LUNCHVOTE', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    db = get_db()
    cur = db.execute('SELECT id,title,description,street,count FROM restaurants ORDER by title ASC')
    out = []
    for row in cur.fetchall():
        out.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'street': row[3],
            'count': row[4]
        })
    return json.dumps(out)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    db = get_db()
    if request.method == 'GET':
        cur = db.execute('SELECT email,name FROM employees ORDER BY name ASC')
        out = []
        for row in cur.fetchall():
            out.append({
                'email': row[0],
                'name': row[1],
            })
        return json.dumps(out)
    else:
        try:
            values = (request.form['email'], request.form['name'])
            db.execute('INSERT INTO employees (email, name) VALUES (?, ?)', values)
            db.commit()
            return "User created"
        except Exception as e:
            abort(500)


@app.route('/vote', methods=['POST'])
def vote():
    db = get_db()
    try:
        now = datetime.datetime.now()
        values = (now.strftime("%Y-%m-%d"), request.form['email'], request.form['restaurant_id'])
        db.execute('INSERT INTO votes (date, email, restaurant_id) VALUES (?, ?, ?)', values)
        # Update count
        db.execute('UPDATE restaurants SET count = count + 1 WHERE id = ?', (request.form['restaurant_id']))
        db.commit()
        return "Sucessfully added vote"
    except Exception as e:
        print e
        abort(500)


@app.route('/splitting', methods=['POST'])
def splitting():
    db = get_db()
    try:
        data = json.loads(request.form['data'])
        print data
        for row in data:
            print row
            db.execute('UPDATE restaurants SET count = count - ? '
                       'WHERE id = ? AND count >= ?', (row['count'], row['restaurant_id'], row['count']))
            db.commit()
        return "Splitting successful"
    except Exception as e:
        print e
        abort(500)


@app.route('/lunch', methods=['POST'])
def lunch():
    db = get_db()
    try:
        cur = db.execute('SELECT id, title FROM restaurants ORDER BY count DESC, RANDOM() LIMIT 1')
        restaurant = cur.fetchone()
        # print restaurant
        # print restaurant[0]
        db.execute('UPDATE restaurants SET count = 0 WHERE id = ?', (str(restaurant[0])))
        db.commit()
        return str(restaurant[0])
    except Exception as e:
        print e
        abort(500)


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response