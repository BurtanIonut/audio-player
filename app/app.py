from typing import List, Dict
from flask import Flask
import mysql.connector
import json
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

def insert_data():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'knights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO favorite_colors (name, color) VALUES (\'Lancelot\', \'blue\'), (\'Galahad\', \'yellow\');')
    cursor.close()
    connection.commit()
    connection.close()
    return

def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'knights'
    }
    insert_data()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()
    return results

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Already logged in'


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        output = json.dumps({'favorite_colors': favorite_colors()})
        return render_template('admin.html',output=output)
    else:
        flash('wrong password!')
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/admin')
def script_output():
    output = json.dumps({'favorite_colors': favorite_colors()})
    return render_template('template_name.html',output=output)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0')