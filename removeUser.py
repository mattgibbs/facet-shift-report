from app import db, models
import sys

allUsers = models.User.query.order_by(models.User.name)

print "Current users: "
for u in allUsers:
	sys.stdout.write(u.name + ", ")
print ""
userToDelete = raw_input("Please enter user to delete (by user name; e.g. E201): ")

user = models.User.query.filter_by(name = userToDelete).first()
if user != None and user.name == userToDelete:
	confirm = raw_input("Found user " + userToDelete + ". Delete? [Y/N]: ")
	if confirm[0] == "Y" or confirm[0] == "y":
		db.session.delete(user)
		db.session.commit()
		print "User " + userToDelete + " deleted."
else:
	print "User " + userToDelete + " not found."