
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

usr        = "ubuntu"          # Username for database
database   = "printers"        # Name of database
printTable = "printers"        # Name of table for printers
errorTable = "errors"          # Name of table for errors
idTable    = "ids"             # Name of table for assigning ids


## Given a printer buildingName, roomNumber, and any other data about a printer, updates the corresponding printer record
## Forces an update if force is true; otherwise, depends on whether an error is set; if not, the record is updated. if so,
## the record is only allowed to update if the current time minus the time it was last updated is larger than minTime
def updatePrinter(buildingName, roomNumber, force = 0, status = None, latitude = None, longitude = None, 
	altitude = None):
	
	update = force
	locVal = (buildingName, roomNumber)
	loc    = ("buildingName", "roomNumber")
	# Query error table for errors with this printer that are not cleared; if not, set update to true

	# Error reported for printer - compare timestamps
	#if !update:

	if update: 

		if status != None:
			updateRecord(printTable, "status", status, loc, locval)

		if latitude != None:
			updateRecord(printTable, "latitude", latitude, loc, locval)

		if longitude != None:
			updateRecord(printTable, "longitude", longitude, loc, locval)

		if altitude!= None:
			updateRecord(printTable, "altitude", altitude, loc, locval)

		if buildingName != None:
			updateRecord(printTable, "buildingName", buildingName, loc, locval)

		if roomNumber != None:
			updateRecord(printTable, "roomNumber", roomNumber, loc, locval)

## Updates the value of column in table for the with an identifier column that has the value idVal
## All SQL updating should happen through this function. 
## If the specified field does not exist, creates a row for it.
## Note that usage of %s in python causes automatic escaping
def updateRecord(table, columns, values, ids, idVals):

	cnx    = mysql.connector.connect(user=usr, database=database)
	cursor = cnx.cursor()
	constraints = " AND ".join("%s=%s" % a for a in zip(ids, idVals));
	data   = (table, constraints);

	# check if the key with identifier=idVal is in the table; if not, it needs to be inserted
	cmd  = "SELECT 1 FROM %s WHERE %s"

	# record exists
	if (cursor.execute(cmd), data):
		c = ", ".join("%s=%s" % a for a in zip(columns, values));
		cmd  = "UPDATE %s SET %s WHERE %s"
		data = (table, c, constraints)

	# record does not exist - create it
	else:
		i = ", ".join(ids.append(columns))      # columns
		v = ", ".join(idVals.append(values))    # values
		cmd  = "INSERT INTO %s (%s) VALUES (%s)"
		data = (table, i, v)
	
	cursor.execute(cmd, data)
	cnx.commit()
	cursor.close()
	cnx.close()


## SQL getting should happen through this function. 
## Note that usage of %s in python causes automatic escaping
def getRecord(table, column, identifier, idVal):
	cnx    = mysql.connector.connect(user=usr, database=database)
	cursor = cnx.cursor()
	data   = (table, identifier, idVal)

	# check if the key with identifier=idVal is in the table; if not, it needs to be inserted
	cmd  = "SELECT 1 FROM %s WHERE %s=%s"

	# record exists
	if (cursor.execute(cmd), data):
		cmd = "SELECT %s from %s WHERE %s=%s"
		data = (table, column, identifier, idVal)
		val = cursor.execute(cmd, data)

	# record does not exist
	else:
		val = 0;
	
	cursor.execute(cmd, data)
	cnx.commit()
	cursor.close()
	cnx.close()
	return val

updatePrinter("White House", "Baracks Room", force=1);