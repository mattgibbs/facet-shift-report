import sqlite3

conn = sqlite3.connect('test1.db')
c = conn.cursor()
fake_goals = '* Conquer World\n* Make Sandwich'
fake_progress = '* Aligned laser\n* Created blackhole'
fake_problems = "* Blackhole destroyed Earth\n*I'm dead"
fake_next_shift = "*I'm dead"
fake_summary = "*Died"

line = ('E201', 'Swing', 'David', fake_goals, fake_progress, fake_problems, fake_next_shift, fake_summary, '', 8, 0, "I don't know", 100)

c.execute('''CREATE TABLE shift_reports (usergroup text, shift text, personnel text, goals text, 
			progress text, problems text, next_shift text, brief_summary text, other text, 
			useful_beam_time real, unscheduled_accelerator_down real, other_down_reason text, 
			accelerator_physicist_availability real)''')
c.execute("INSERT INTO shift_reports VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", line)

conn.commit()
conn.close()


'''
PROGRAM:
usergroup
shift
personnel

SUMMARIES:
goals
progress
problems
next_shift
brief_summary
other

TIME ACCOUNTING:
useful_beam_time
unscheduled_accelerator_down
other_down_reason
accelerator_physicist_availability'''