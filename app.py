import ConfigParser
import os
import sys

from flask import Flask, flash, jsonify, render_template, request, redirect, url_for

from connection import session
from database_setup import DuesRecord

from create_db import main as update_database

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def homepage():
    name = ''
    due = ''
    result = ''
    if request.method == 'GET':
        return render_template('homepage.html',result = result, date = app.config['DATE'])
    elif request.method == 'POST':
        roll_no = request.form['roll_no'].encode('ascii').upper()
        try:
            record = session.query(DuesRecord).filter_by(roll_no = roll_no).one()
            name, due = record.name, record.due
            return render_template('homepage.html',name = name, due = due, result = '', date = app.config['DATE'])        
        except:
            result = "Invalid roll number!"
            return render_template('homepage.html',name = 'NA', due = 0, result = result, date = app.config['DATE'])        
    else:
        pass 

@app.route('/<roll_no>')
def homepageJSON(roll_no):
	roll_no	= roll_no.encode('ascii').upper()
	try:
	    record = session.query(DuesRecord).filter_by(roll_no = roll_no).one()
	    return jsonify(due=record.serialize)          
	except:
	    return '''
            Format: &nbsp&nbsp&nbsp&nbsp hostel-dues.herokuapp.com/&lt;roll_no&gt;''' + '<br>' + '''Example: &nbsp hostel-dues.herokuapp.com/b150487cs'''

@app.route('/update', methods = ['GET','POST'])
def updateDatabase():
    if request.method == 'GET':
        return render_template('updatepage.html', date = app.config['date']) 
    elif request.method == 'POST':
        if 'password' in request.form:
            if request.form['password'] == 'b150487CS@1':
                update_database()
                fetchLastUpdateDetails()
                return redirect(url_for('homepage'))
            else:
                return render_template('homepage.html', date = app.config['date'])
    else:
        pass 

def fetchLastUpdateDetails():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    day = config.get('Last_Update','date')
    month = config.get('Last_Update','month')
    year = config.get('Last_Update','year')
    app.config['DATE'] = day + '/' + month + '/' + year

def main():
    fetchLastUpdateDetails()
    app.secret_key = 'theQuickBrownFoxJumpsOverTheLazyDog'
    if len(sys.argv) > 1:
        if sys.argv[1] == 't':
            app.debug = True
    port = int(os.environ.get('PORT',8000))
    app.run(host = '0.0.0.0',port = port) 

if __name__ == "__main__":
    main()
