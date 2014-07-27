from app import db, models

userToAdd = raw_input("Please enter user to create (by user name; e.g. E201): ")

user = models.User.query.filter_by(name = userToAdd).first()
if user != None:
	print "User " + userToAdd + " already exists."
else:
	confirm = raw_input("Create user " + userToAdd + "? [Y/N] : ")
	if confirm[0] == "Y" or confirm[0] == "y":
		u = models.User(name=userToAdd)
		db.session.add(u)
		db.session.commit()
		print "User " + userToAdd + " added."