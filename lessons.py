from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_login import LoginManager, login_required
from sqlite3 import connect, Row
from helpers import get_db, login_required
from app import app

# Lessons
@app.route('/lessons')
@login_required
def lessons():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    return render_template('lessons.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Lesson 1
@app.route('/lessons/1')
@login_required
def lesson1():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    if progress['lessons_completed'] == 0:
        db.execute('UPDATE users SET lessons_completed = lessons_completed + 1 WHERE id = ?', (session['user_id'],))
        db.execute(
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 2, CURRENT_TIMESTAMP, ?)',
                (session['user_id'],))
        connection.commit()

    return render_template('lesson1.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

# Lesson 2
@app.route('/lessons/2')
@login_required
def lesson2():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    if progress['lessons_completed'] == 1:
        db.execute('UPDATE users SET lessons_completed = lessons_completed + 1 WHERE id = ?', (session['user_id'],))
        db.execute(
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 1, CURRENT_TIMESTAMP, ?)',
                (session['user_id'],))
        connection.commit()

    return render_template('lesson2.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Lesson 3
@app.route('/lessons/3')
@login_required
def lesson3():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    if progress['lessons_completed'] == 2:
        db.execute('UPDATE users SET lessons_completed = lessons_completed + 1 WHERE id = ?', (session['user_id'],))
        db.execute(
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 2, CURRENT_TIMESTAMP, ?)',
                (session['user_id'],))
        connection.commit()

    return render_template('lesson3.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])