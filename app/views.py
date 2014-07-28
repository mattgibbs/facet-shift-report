from flask import render_template, flash, redirect, url_for
from app import app, db, models
from forms import LoginForm
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
def shift_summary_form():
	form = LoginForm()
	form.setForm()
	if form.validate_on_submit():
		try:
			print form.data
			report = models.ShiftReport(form)
			db.session.add(report)
			db.session.commit()
			flash("Successfully uploaded to database!")
		except :
			flash("Error")
		return redirect('/')
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