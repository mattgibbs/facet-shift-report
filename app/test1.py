from flask import Flask, render_template, request, redirect
import time
import sqlite3
from formData import form_data

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('test.html', entries=get_shift_entries())

@app.route('/shift_summary_form/', methods=['GET', 'POST'])
def shift_summary_form():
    if request.method == 'GET':
        return render_template('shift_summary_form.html')
    else:
        enter_submitted_form(request.form)
        return redirect('/')

@app.route('/shift_summaries')
def shift_view():
    return render_template('test.html', entries=get_shift_entries())

def enter_submitted_form(form):
    f = form_data(form)
    line = f.get_tuple()
    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    c.execute("INSERT INTO shift_reports VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
    conn.commit()
    conn.close()

def get_shift_entries():
    conn = sqlite3.connect('test1.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM shift_reports')
    shift_reports = get_all_reports(c)
    conn.close()
    return shift_reports

def get_all_reports(cursor):
    pass
    shift_reports = []
    while True:
        next_row = cursor.fetchone()
        if next_row == None:
            break
        shift_reports.append(form_data(next_row)) # Create a form data object and immediately convert to tuple
    return shift_reports
	

if __name__ == "__main__":
    app.run(debug = True)