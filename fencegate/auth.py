import functools

from .dummy import _
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pass2 = request.form['pass2']
        db = get_db()
        error = None

        if not username:
            error = 'Please input a Username'
        elif not password:
            error = 'Please specify a password'
        elif pass2 != password:
            error = 'The passwords do not match'
        elif db.execute('SELECT * FROM user WHERE username=?', (username, )).fetchone() is not None:
            error = "The username {} already exists".format(username)

        if error is None:
            db.execute(
                'INSERT INTO user(username, password) VALUES (?, ?)',
                (username, generate_password_hash(pass2))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(_(error))

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if (user is None) or (not check_password_hash(user['password'], password)):
            error = 'The username password combination is not recognized'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(_(error))

    return render_template('auth/login.html')


@bp.before_app_request
def get_logged_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id=?", (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
