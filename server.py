""" A sample server. """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import User
from model import connect_to_db, db
import bcrypt

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage. """

    return render_template("index.html")


@app.route('/register')
def register():
    """ Renders register template form. """

    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register_process():
    """ Register a new user. """

    username = request.form.get("username")
    password = request.form.get("password")
    password = password.encode('utf8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    new_user = User(username=username, password=hashed)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


@app.route('/login')
def login_page():
    """ Renders login page. """

    return render_template('/login.html')


@app.route('/login', methods=['POST'])
def login_process():
    """ Checks if credentials are correct and redirects to homepage. """

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.username == username).first()
    if user:
        if bcrypt.checkpw(password, user.password):
            return redirect('/')

    flash("Email/password combination do not match.")
    return redirect('/login')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
