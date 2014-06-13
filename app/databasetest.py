import sqlite3

conn = sqlite3.connect('test1.db')

conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT * FROM shift_reports')
form = c.fetchone()
print form.keys()

usergroup = form['usergroup']
shift = form['shift']
personnel = form['personnel']
goals = form['goals']
progress = form['progress']
problems = form['problems']
next_shift = form['next_shift']
brief_summary = form['brief_summary']
other = form['other']
useful_beam_time  = form['useful_beam_time']
unscheduled_accelerator_down = form['unscheduled_accelerator_down']
other_down_reason = form['other_down_reason']
accelerator_physicist_availability = form['accelerator_physicist_availability']
print (usergroup, shift, personnel, goals, progress,
		problems, next_shift, brief_summary, other,
		useful_beam_time, unscheduled_accelerator_down,
		other_down_reason, accelerator_physicist_availability)





conn.close()