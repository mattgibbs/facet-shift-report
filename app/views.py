from flask import render_template, flash, redirect
from app import app, db, models
from forms import LoginForm
import datetime

@app.route('/')
def index():
	posts = [
		{
			'author': {'nickname': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'nickname': 'Sarah'},
			'body': 'The Avengers movie was so cool!'
		},
		]
	return render_template("index.html", posts=posts)


@app.route('/shift_summary_form/', methods=['GET', 'POST'])
def shift_summary_form():
	form = LoginForm()
	form.setForm()
	if form.validate_on_submit():
		try:
			print form.data
			report = models.ShiftReport(form)
			db.session.add(report)
			db.session.commit()
			flash("Successfully uploaded to database")
		except :
			flash("Error")
		return redirect('/')
	return render_template('shift_report.html', form=form)