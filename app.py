import os
import sys

from flask import Flask, flash, render_template, request, jsonify

from connection import session
from database_setup import DuesRecord

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def homepage():
    name = ''
    due = ''
    result = ''
    if request.method == 'GET':
        return render_template('homepage.html',result = result)
    elif request.method == 'POST':
        roll_no = request.form['roll_no'].encode('ascii').upper()
        try:
            record = session.query(DuesRecord).filter_by(roll_no = roll_no).one()
            name, due = record.name, record.due
            return render_template('homepage.html',name = name, due = due, result = '')        
        except:
            result = "Invalid roll number!"
            return render_template('homepage.html',name = 'NA', due = 0, result = result)        
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

def main():
    app.secret_key = 'fbjsdbfjlabsdkjbsjdk'
    # print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == 't':
            app.debug = True
    port = int(os.environ.get('PORT',8000))
    app.run(host = '0.0.0.0',port = port) 

if __name__ == "__main__":
    main()
