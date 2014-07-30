from flask import render_template, flash, redirect, url_for
from app import app, db, models
from forms import LoginForm, UserForm
import datetime

@app.errorhandler(404)
def internalerror(error):
	return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
	reports = models.ShiftReport.query.order_by('id desc').all()
	return render_template("index.html", reports=reports)


@app.route('/shift_summary_form/', methods=['GET', 'POST'])
@app.route('/shift_summary_form/<int:reportid>', methods=['GET', 'POST'])
def shift_summary_form(reportid = None):
	form = LoginForm()
	form.setForm()
	if form.validate_on_submit():
		try:
			if reportid:
				report = models.ShiftReport.query.get(reportid)
				report.read_form(form)
			else:
				report = models.ShiftReport(form)
				db.session.add(report)
			db.session.commit()
			flash("Successfully uploaded to database")
		except:
			flash("Error uploading to database")
		return redirect('/')
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			# Fill out form with data from database
			print report.user
			form.read_report(report)
			print form.user.data
		else:
			# Report ID does not exist
			flash("Report does not exist")
			return redirect('/shift_summary_form/')
	print form.user.data
	return render_template('shift_report.html', form=form)

@app.route('/view_report/<int:reportid>')
def view_report(reportid = None):
	print reportid
	if reportid:
		report = models.ShiftReport.query.get(reportid)
		if report:
			return render_template('view_report.html', report=report)
		else:
			flash("Failed to load report #" + str(reportid) + ". Report does not exist.")
			return redirect('/')
	flash("Redirected to root.")
	return redirect('/')

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
	form = UserForm()
	if form.validate_on_submit():
		try:
			user = models.User(form)
			db.session.add(user)
			db.session.commit()
			flash("Successfully created user " + form.data['userName'])
		except:
			flash("Error creating user. Exception " + type(e))
		
		return redirect('/')
	return render_template('create_user.html', form=form)