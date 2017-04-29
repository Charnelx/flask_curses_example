from functools import wraps
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, url_for, redirect, \
     render_template, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
from werkzeug.routing import BaseConverter

# app settings
# DATABASE = 'db/db.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'key123'

# app initialisation
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('EXAPP_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# Use the RegexConverter function as a converter
# method for mapped urls
app.url_map.converters['regex'] = RegexConverter

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('SELECT * FROM user WHERE user_id = ?',
                          [session['user_id']], one=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('SELECT user_id FROM user WHERE username = ?',
                  [username], one=True)
    return rv[0] if rv else None

@app.route('/id_<regex("\d+"):id>/')
def detail(id):
    '''Example of regex use in routes'''
    topic = query_db('''SELECT * FROM topics WHERE
                _id = ?''', id, one=True)
    return ''

@app.route('/', methods=['GET'])
@login_required
def home_page():
    """Displays topics"""
    if request.method == 'GET':
        topics = query_db('''SELECT * FROM topics''')
        return render_template('index.html', topics=topics)

@app.route('/', methods=['POST'])
@login_required
def home_page_post():
    """Render results"""
    if request.method == 'POST':
        search_query = request.form['text']
        print(search_query)
        if search_query:
            topics = query_db('''SELECT * FROM topics
                                WHERE title IN (
                                    SELECT title FROM topics WHERE lower(title) LIKE lower(?)
                                UNION
                                    SELECT title FROM topics WHERE lower(author) LIKE lower(?)
                                );''', ('%' + search_query + '%',) * 2)
            if topics:
                return render_template('results.html', topics=topics)
    return render_template('results.html', topics=[])




@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('home_page'))
    error = None
    if request.method == 'POST':
        user = query_db('''SELECT * FROM user WHERE username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('home_page'))
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
    """Logout user."""
    if session.get('user_id', None):
        session.clear()
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('home_page'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''INSERT INTO user (
              username, email, pw_hash) VALUES (?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.debug = DEBUG
    app.run()