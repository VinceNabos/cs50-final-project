# Syntax
#### Video Demo: <URL HERE>
#### Description:

## Summary:
#### Syntax is a website that introduces basic programming concepts with Python using lessons and exercises
#### (inspired by CS50x, Leetcode, and w3Schools).

## Technology:
#### The program has a frontend made with HTML, CSS, and JavaScript, with help from Bootstrap's library.
#### The program has a backend made with Python, Flask, Jinja, and sqlite3.
#### The program has a database for user information managed by SQLite.

## Personal Choices:
### The idea for my final project was clear from the start: a piece of software that introduced programming in a non-intimidating way. Originally, I wanted to make a game for my CS50x final project where you use coding concepts to move a character. However, after weighing my options, I went with a coding website.
### One, I had to accept my limitations. As much as I wanted the final project to be something made for deployment or launch, I had limited time and was not confident enough to learn what I needed to learn in such a short timeframe. Freshman year was coming up and I wanted to finish CS50x before that to focus on my academics.
### Two, I wanted to do something related to my future career interests. My dream is to someday use my degree to contribute to the AI/ML scene in the Philippines. Sadly, I couldn't find a way to train my data or AI/ML skills with a game, so I went with a website instead.

## Limitations:
### While Syntax's exercises have code editors that can successfuly run Python, they are extremely sensitive. One wrong program and boom, site is probably dead.
### Prevention systems were added, such as preventing infinite loops or imports, but the code a user writes is still run locally instead of in a virtual environment.
### Exercise checking was also extremely sensitive. Test cases had to be specified in the instructions to prevent correct answers being markd incorrect due to the wacky code checker.
### There are also no code editors outside of the exercises, meaning users had to download Python themselves (or explore other ways) to test out their Python skills. Though, in a way, this does teach the user how to keep learning when it comes to the world of computer science, which is nice in a way.

## Project Structure:
### app.py
#### app.py is the main backend of Syntax. It contains all Flask routes and application logic, including user authentication, lesson navigation, exercise validation, dashboard functionality, and account management. The file acts as the central controller of the application, processing requests from users, interacting with the database, and rendering the appropriate templates.
### helpers.py
#### helpers.py contains helper functions that are reused throughout the project. This includes the utility functions for database access and login protection and authentication.
### temp.py
#### temp.py is responsible for safely executing user-submitted Python code for exercises. When a user submits a solution, the program temporarily stores and runs their code inside a controlled environment. The output is then compared against expected results or test cases to determine whether the exercise was completed successfully. This file allows Syntax to provide an interactive coding experience directly in the browser.
### users.db
#### users.db is the SQLite database used by the application. It stores user accounts, authentication information, lesson and exercise progress, and user history. By storing information in a database, Syntax is able to remember a user's progress between sessions and provide a personalized learning experience.
### templates/
#### The templates directory contains all HTML files used by the application. Syntax uses Flask's Jinja templating engine, allowing dynamic content to be rendered based on information from the backend. Pages such as the dashboard, lessons, exercises, login page, registration page, and account page are all stored within this directory.
### static/
#### The static directory contains all frontend assets used by Syntax. This includes CSS stylesheets, JavaScript files (mainly used for highlights.js), and images that define the appearance and behavior of the website. Separating static files from templates keeps the project organized and follows Flask's recommended project structure.

## Authentication:
#### The program has a simple registration and login system. This ensures that users' progress are tracked and stored properly inside of a database. When a user is not logged in, they cannot access the website's features. If a user does not have an account, they have to register with a unique username and password.

## Dashboard and Account:
#### The dashboard has three main components: the welcome text, continue menu, and progress bar. 
#### The welcome text is a simple heading that welcomes users into Syntax, serving as a casual, non-intimidating sight when opening the site. 
#### The continue menu serves to provide quick and easy access to the last lesson and exercise that the user has done, improving upon UX. 
#### The progress bar shows a user's current lesson and exercise progress, serving as a motivation for new users and giving a sense of accomplishment for users that have completed all activities.
#### The accounts page serves as the home of the user's history, and the ability to change username and passwords.

## Lessons:
### Lesson 1: Variables, Data Types, Operators
#### Lesson 1 introduces the fundamental building blocks of programming and programming in Python. Users learn how to store information using variables, work with different data types such as integers, floats, strings, and booleans, and manipulate data using arithmetic and comparison operators. These concepts serve as the foundation for all future lessons and exercises, and will be fundamental for the user's future in programming.
### Lesson 2: Conditionals, Loops
#### Lesson 2 introduces program flow through conditionals and loops. Users learn how computers make decisions using conditional statements such as if, elif, and else statements, as well as how to repeat tasks efficiently using for and while loops. These concepts allow programs to respond to different inputs and perform repetitive actions without duplicating code, allowing for more elegant solutions.
### Lesson 3: Lists, Dictionaries
#### Lesson 3 introduces Python's most common data structures: lists and dictionaries. Users learn how to store and organize collections of data, access individual elements, modify existing values, and iterate through structured information. These concepts are essential for building more complex programs and provide the foundation for other computer science concepts down the road.

## Exercises:
### Exercise 1.1: Change
#### In this exercise, users create a function that calculates the amount of change to return after a purchase. The exercise reinforces the use of variables, functions, arithmetic operators, and printing values. As the firstsexercises in Syntax, it is designed to familiarize users with writing simple Python functions.
### Exercise 1.2: Profiling
#### This exercise challenges users to create a simple profile using information provided as inputs. Users practice working with variables and strings by combining multiple texts into a single output. The exercise reinforces the concept of storing and manipulating data while introducing basic string operations.
### Exercise 2.1: FizzBuzz
#### FizzBuzz is a classic programming exercise that requires users to print a sequence of numbers while applying special rules to certain values. Multiples of three become "Fizz", multiples of five become "Buzz", and multiples of both become "FizzBuzz". The exercise reinforces conditionals, loops, and logical thinking.
### Exercise 2.2: Secretary
#### In this exercise, users create a schedule tracker that determines a boss' current task based on the day and time. The exercise focuses on conditional statements and decision-making logic, requiring users to evaluate multiple rules in the correct order to produce the appropriate task.
### Exercise 3.1: Where's Waldo
#### Where's Waldo introduces users to dictionaries by asking them to locate specific information within a list of key-value pairs. The exercise reinforces dictionary access and retrieval while demonstrating how structured data can be stored and searched efficiently in Python.
### Exercise 3.2: Register
#### Register serves as the final exercise of Syntax and combines multiple concepts introduced throughout the course. Users work with a list representing existing user accounts and determine whether a proposed username is valid through various checks. The exercise reinforces loops, conditionals, arrays, and data validation, making it one of the most comprehensive challenges for users.