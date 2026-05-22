from sqlite3 import connect, Row
from functools import wraps
from flask import request, redirect, session


def get_db():
    connection = connect('users.db')
    connection.row_factory = Row
    return [connection, connection.cursor()]


# Login required decorator from https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/ and https://cs50.harvard.edu/x/psets/9/finance/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
