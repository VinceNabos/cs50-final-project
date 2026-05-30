# SQL Library
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_required
from sqlite3 import connect, Row
from helpers import get_db, login_required
from subprocess import run, TimeoutExpired
from ast import parse, walk, Import, ImportFrom, literal_eval
from random import randint, uniform, choice

# Configure app
app = Flask(__name__)
app.secret_key = b'7ed559e13e3e66b64cc32d87488776c91fdc6b65d9f9d8d1ff29aa97621ee91f'

# Dashboard and home
@app.route('/')
@login_required
def dashboard():

    # Execute database
    sql = get_db()
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    return render_template('dashboard.html', username=session['username'], progress=progress)


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
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 1, CURRENT_TIMESTAMP, ?)',
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
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 2, CURRENT_TIMESTAMP, ?)',
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
                'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (0, 3, CURRENT_TIMESTAMP, ?)',
                (session['user_id'],))
        connection.commit()

    return render_template('lesson3.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Exercises
@app.route('/exercises')
@login_required
def exercises():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    return render_template('exercises.html', 
                           lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Set 1: Exercise 1
@app.route('/exercises/1/change', methods=['GET', 'POST'])
@login_required
def exercise1():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method is POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/1/change')

        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise1.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise1.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            for i in range(3):    
                price = round(uniform(1, 20), 2)
                cash = round(uniform(20, 50), 2)
                test = '\nchange({x}, {y})'
                code_test += test.format(x = price, y = cash)
                answers.append(cash - price)    

            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise1.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise1.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = result.stdout.splitlines()

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise1.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 3:
            return render_template('exercise1.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 3:
            return render_template('exercise1.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(3):
            try:
                if float(outputs[i]) != answers[i]:
                    return render_template('exercise1.html', code=code, output=output, 
                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
            except ValueError:
                return render_template('exercise1.html', code=code, output='ValueError',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 0:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 1, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()

            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise1.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
    
    # Load website if method is GET
    else:
        return render_template('exercise1.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
    

# Set 1: Exercise 2
@app.route('/exercises/1/profiling', methods=['GET', 'POST'])
@login_required
def exercise2():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method was POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/1/profiling')
        
        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise2.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise2.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            for i in range(3):    
                names = [
                    'Harp', 'Robin', 'Kai', 'Luca', 'Hanabi',
                    'Angel', 'Harper', 'Park', 'Mitsu', 'Jamie'
                    ]
                name = choice(names)
                age = randint(1, 100)
                sexes = ['M', 'F']
                sex = choice(sexes)
                test = '\nprofiling("{x}", {y}, "{z}")'
                code_test += test.format(x = name, y = age, z = sex)
                answers.append(f'{name} {age}{sex}')    

            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise2.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise2.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = result.stdout.splitlines()

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise2.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 3:
            return render_template('exercise2.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 3:
            return render_template('exercise2.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(3):
            if outputs[i] != answers[i]:
                return render_template('exercise2.html', code=code, output=output, 
                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 1:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 2, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()
            
            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise2.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


    else:
        return render_template('exercise2.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Set 2: Exercise 1
@app.route('/exercises/2/fizzbuzz', methods=['GET', 'POST'])
@login_required
def exercise3():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method was POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/2/fizzbuzz')
        
        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise3.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise3.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            code_test += '\nfizzbuzz(100)'
            for n in range(1, 101):
                if n % 3 == 0 and n % 5 == 0:
                    answers.append('FizzBuzz')
                elif n % 3 == 0:
                    answers.append('Fizz')
                elif n % 5 == 0:
                    answers.append('Buzz')
                else:
                    answers.append(str(n))

            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise3.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise3.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = result.stdout.splitlines()

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise3.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 100:
            return render_template('exercise3.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 100:
            return render_template('exercise3.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(len(answers)):
            if outputs[i] != answers[i]:
                return render_template('exercise3.html', code=code, output=output, 
                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 2:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 3, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()
            
            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise3.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

    else:
        return render_template('exercise3.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Set 2: Exercise 2
@app.route('/exercises/2/secretary', methods=['GET', 'POST'])
@login_required
def exercise4():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method was POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/2/secretary')
        
        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise4.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise4.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            for i in range(3):    
                times = [
                    'morning', 'lunch', 'afternoon', 'evening'
                    ]
                day = randint(1, 7)
                time = choice(times)
                test = '\nsecretary({x}, "{y}")'
                code_test += test.format(x = day, y = time)

                # Secretary answers
                if day == 1 or day == 7:
                    answers.append('weekend')
                elif time == 'lunch':
                    answers.append('break')
                elif time == 'morning':
                    answers.append('standup')
                elif time == 'evening':
                    answers.append('clock-out')
                elif time == 'afternoon':
                    if day in [2, 4, 6]:
                        answers.append('client')
                    else:
                        answers.append('paperwork')

            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise4.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise4.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = result.stdout.splitlines()

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise4.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 3:
            return render_template('exercise4.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 3:
            return render_template('exercise4.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(3):
            if outputs[i] != answers[i]:
                return render_template('exercise4.html', code=code, output=output, 
                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 3:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 4, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()
            
            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise4.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

    else:
        return render_template('exercise4.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Set 3: Exercise 1
@app.route('/exercises/3/waldo', methods=['GET', 'POST'])
@login_required
def exercise5():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method was POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/3/waldo')
        
        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise5.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise5.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            names = [
                'Harp', 'Robin', 'Kai', 'Luca', 'Hanabi',
                'Angel', 'Harper', 'Park', 'Mitsu', 'Waldo'
            ]
            cities = [
                'Sausage Town', 'Pickle Town', 'Waffle Land', 'Noodle City',
                'Burger Town', 'Donut Land', 'Muffin City', 'Potato City',
                'Banana Town', 'Biscotti Land'
            ]
            disguises = [
                'Cop', 'Lifeguard', 'Hotdog Vendor', 'Clown', 'Teacher',
                'Professional Yodeler', 'Singer', 'Dancer', 'Student', 'Unemployed'
            ]

            # Three test cases
            for i in range(3):    
                
                people = []

                # Five dictionaries
                for i in range(5):
                    person = {}
                    if i == 4 and not any(name['name'] == 'Waldo' for name in people):
                        person['name'] = 'Waldo'
                    else:
                        person['name'] = choice(names)
                    person['city'] = choice(cities)
                    person['disguise'] = choice(disguises)
                    people.append(person)
                
                test = '\nwaldo({x})'
                code_test += test.format(x = people)


                # Waldo answers
                for i in range(len(people)):
                    if people[i]['name'] == 'Waldo':
                        answers.append([
                            people[i]['name'],
                            people[i]['city'],
                            people[i]['disguise']
                        ])
                        break
                

            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise5.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise5.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = [
                literal_eval(line)
                for line in result.stdout.splitlines()
            ]

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise5.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 3:
            return render_template('exercise5.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 3:
            return render_template('exercise5.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(3):
            if outputs[i] != answers[i]:
                return render_template('exercise5.html', code=code, output=output, 
                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 4:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 5, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()
            
            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise5.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

    else:
        return render_template('exercise5.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Set 3: Exercise 2
@app.route('/exercises/3/register', methods=['GET', 'POST'])
@login_required
def exercise6():

    # Execute database
    sql = get_db()
    connection = sql[0]
    db = sql[1]

    # Load user progress
    db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
    progress = db.fetchone()

    # Run code if method was POST
    if request.method == 'POST':

        # Reset website if reset was pressed
        if request.form.get('action') == 'reset':
            return redirect('/exercises/3/register')
        
        # Get code
        code = request.form.get('code').rstrip()

        # Check code for imports
        try:
            tree = parse(code)
            for node in walk(tree):

                if isinstance(node, (Import, ImportFrom)):
                    return render_template('exercise6.html', code=code, output='For safety reasons, imports are not allowed!',
                                        lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Returns error
        except SyntaxError as output:
            return render_template('exercise6.html', code=code, output=output, 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Variables for checking
        outputs = []
        answers = []

        # Execute code
        try:

            # Testing code
            code_test = code

            # Test cases
            usernames = [
                'NovaRift',   'ByteLynx',   'FrostByte',  'LunarZip',   'NeonDrift',    # Has 10 duplicates
                'RapidVibe', 'VaporNest',  'ZenithBug',  'BlazeRoot',  'CyberMoth',
                'AquaPulse',  'BrickNova', 'CopperWing', 'DriftPixel', 'EmberKick',
                'FluxRider',  'GhostLeaf',  'HyperSeed', 'IvoryDash',  'JoltCrate',
                'KarmaBlink', 'LogicSpark', 'MegaTrail',  'NitroFang', 'OmegaClaw',
                'PrismVolt',  'QuartzNeko', 'RogueFrame', 'StaticPine', 'TitanBloom',
                'space name', 'space name', 'space name', 'space name', 'space name',   # Invalid, no spaces
                'space name', 'space name', 'space name', 'space name', 'space name',   # Invalid, no spaces
                'aaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa',             # Invalid, not 1-15
                'aaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa', '', '', '', '', '',             # Invalid, not 1-15
            ]
            users = [
                'NovaRift', 'PixelFox', 'AeroMint', 'ByteLynx', 'CrimsonIQ',
                'EchoVale', 'FrostByte', 'GlintRush', 'HexaBloom', 'IronPulse',
                'JadeCircuit', 'KiloNova', 'LunarZip', 'MysticOrb', 'NeonDrift',
                'OrbitCraze', 'PlasmaJet', 'QuantumYak', 'RapidVibe', 'SolarNix',
                'TurboLeaf', 'UltraPebble', 'VaporNest', 'WildComet', 'XenonTrail',
                'YellowFlux', 'ZenithBug', 'AlphaTwig', 'BlazeRoot', 'CyberMoth',
            ]

            # Three test cases
            for i in range(3):    
                
                username = choice(usernames)
                
                test = '\nregister("{x}", {y})'
                code_test += test.format(x = username, y = users)

                # Check if username exists
                if username in users:
                    answers.append('Invalid: Username already exists')
                # Check if username has spaces
                elif ' ' in username:
                    answers.append('Invalid: Username cannot have spaces')
                elif not username or len(username) < 1 or len(username) > 15:
                    answers.append('Invalid: Username must be 1-15 characters long')
                else: answers.append('Valid')
                
            # Put code inside a file
            with open('temp.py', 'w') as file:
                file.write(code_test)

            result = run(
            ['python', 'temp.py'],
            capture_output=True,
            text=True,
            timeout=5,
            input=''
            )
        
        except TimeoutExpired:
            return render_template('exercise6.html', code=code, output='Code execution timed out!', 
                                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        output = result.stderr
        if output:
            return render_template('exercise6.html', code=code, output=output, 
                lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        else:
            output = result.stdout
            outputs = result.stdout.splitlines()

        # Return if output is empty or not enough
        if not outputs:
            return render_template('exercise6.html', code=code, output='No output detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) > 3:
            return render_template('exercise6.html', code=code, output='Too much outputs detected',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        elif len(outputs) < 3:
            return render_template('exercise6.html', code=code, output='Incomplete number of outputs',
                                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

        # Checks answers
        for i in range(3):
            if outputs[i] != answers[i]:
                return render_template('exercise6.html', code=code, output=output, 
                    lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])
        
        # Update database if correct answer
        if progress['exercises_completed'] == 5:
            db.execute('UPDATE users SET exercises_completed = exercises_completed + 1 WHERE id = ?', (session['user_id'],))
            db.execute(
                    'INSERT INTO history (act_type, act_number, timestamp, user_id) VALUES (1, 6, CURRENT_TIMESTAMP, ?)',
                    (session['user_id'],))
            connection.commit()
            
            # Update progress variable
            db.execute('SELECT lessons_completed, exercises_completed FROM users WHERE id = ?', (session['user_id'],))
            progress = db.fetchone()

        return render_template('exercise6.html', code=code, output=output, correct=True,
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])

    else:
        return render_template('exercise6.html', 
                            lessons_completed=progress['lessons_completed'], exercises_completed=progress['exercises_completed'])


# Account settings
@app.route('/account')
@login_required
def account():

    sql = get_db()
    db = sql[1]

    db.execute('SELECT * FROM history WHERE user_id = ?', (session['user_id'],))
    progress = db.fetchall()

    return render_template('account.html', username=session['username'], history=progress)


# Change username
@app.route('/account/change-username', methods=['GET', 'POST'])
@login_required
def change_username(error=''):

    # Change username if method = 'POST'
    if request.method == 'POST':
        
        # Execute database
        sql = get_db()
        connection = sql[0]
        db = sql[1]

        # Get form responses
        change_username = request.form.get('username')
        confirm_username = request.form.get('confirmUsername')

        # Return error if forms are empty
        if not change_username or not confirm_username:
            return render_template('changeUsername.html', error='Please answer all fields', username=session['username'])
        
        # Return error if forms are not identical
        if change_username != confirm_username:
            return render_template('changeUsername.html', error='Usernames must be identical', username=session['username'])
        
        # Return error if username is the same
        if change_username == session['username']:
            return render_template('changeUsername.html', error='Please choose a new username', username=session['username'])

        # Check existing database for usernames
        db.execute('SELECT username FROM users WHERE username = ?', (change_username,))

        # Return error if username already exists
        if db.fetchone() is not None:
            return render_template('changeUsername.html', error='Usernames already exists')
        
        # Change username
        db.execute('UPDATE users SET username = ? WHERE id = ?', (change_username, session['user_id'],))
        connection.commit()
        session['username'] = change_username
        return redirect('/account')

    # Display change username if method = 'GET'
    else:
        return render_template('changeUsername.html', error=error, username=session['username'])
    

# Change password
@app.route('/account/change-password', methods=['GET', 'POST'])
@login_required
def change_password(error=''):

    # Change password if method = 'POST'
    if request.method == 'POST':
        
        # Execute database
        sql = get_db()
        connection = sql[0]
        db = sql[1]

        # Get form responses
        password = request.form.get('password')
        new_password = request.form.get('newPassword')
        confirm_new_password = request.form.get('confirmNewPassword')

        # Return error if forms are empty
        if not password or not new_password or not confirm_new_password:
            return render_template('changePassword.html', error='Please answer all fields', username=session['username'])
        
        # Return error if password is incorrect
        db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = db.fetchone()
        if not check_password_hash(user['hash'], password):
            return render_template('changePassword.html', error='Incorrect password', username=session['username'])

        # Return error if forms are not identical
        if new_password != confirm_new_password:
            return render_template('changePassword.html', error='Passwords must be identical', username=session['username'])
        
        # Return error if password is the same
        if check_password_hash(user['hash'], new_password):
            return render_template('changePassword.html', error='Please choose a new password', username=session['username'])
        
        # Change password
        db.execute('UPDATE users SET hash = ? WHERE id = ?', (generate_password_hash(new_password), session['user_id'],))
        connection.commit()
        session.clear()
        return redirect('/account')

    # Display change password if method = 'GET'
    else:
        return render_template('changePassword.html', error=error, username=session['username'])


# Login
@app.route('/login', methods=['GET', 'POST'])
def login(error=''):
    
    # Login user if method = 'POST'
    if request.method == 'POST':
        
        # Execute database
        sql = get_db()
        connection = sql[0]
        db = sql[1]

        # Get form answers
        username = request.form.get('username')
        password = request.form.get('password')

        # Return to login page in case of empty forms
        if not username or not password:
            return render_template('login.html', error='(Please answer all forms)')
        
        # Gets user data
        db.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = db.fetchone()
        
        # Returns to login page if user does not exist
        if not account:
            return render_template('login.html', error='(Account does not exist)')
        
        # Returns to login page if password is invalid
        if not check_password_hash(account['hash'], password):
            return render_template('login.html', error='(Invalid password)')
        
        # User class
        session['user_id'] = account['id']
        session['username'] = account['username']
        return redirect('/')
    
    # Show login page if method = 'GET'
    else:
        return render_template('login.html', error=error)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register(error=''):

    # Register user if method = 'POST'
    if request.method == 'POST':

        # Execute database
        sql = get_db()
        connection = sql[0]
        db = sql[1]

        # Get form answers
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        hash = generate_password_hash(password)

        # Return to register page in case of empty forms
        if not username or not password or not confirm_password:
            return render_template('register.html', error='(Please answer all forms)')
        
        # Return to register page if password is not confirmed
        if not password == confirm_password:
            return render_template('register.html', error='(Password and confirmation must be identical)')

        # Return to register page if username already exists
        db.execute('SELECT * FROM users WHERE username = ?', (username,))
        if db.fetchone() is not None:
            return render_template('register.html', error='(Username taken)')
        
        # Executes user data into database
        db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, hash,))
        connection.commit()
        return redirect('/login')
    
    # Show register page if method = 'GET'
    else:
        return render_template('register.html', error=error)
    
# Logout
@app.route('/logout')
def logout():
    
    # Log user out
    session.clear()
    return redirect('/login')