from flask import Flask, render_template, request, flash
from connection import session
from database_setup import DuesRecord
import os

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html')
    elif request.method == 'POST':
        roll_no = request.form['roll_no'].encode('ascii')
        record = session.query(DuesRecord).filter_by(roll_no = roll_no).one()
        flash("Name: " + record.name + '\n')
        flash("Roll No: " + record.roll_no + '\n')
        flash("Due: " + str(record.due) + '\n')
        return render_template('homepage.html')        
    else:
        pass 

def main():
    app.secret_key = 'fbjsdbfjlabsdkjbsjdk'
    # app.debug = True
    port = int(os.environ.get('PORT',8000))
    app.run(host = '0.0.0.0',port = port) 

if __name__ == "__main__":
    main()