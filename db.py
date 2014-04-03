
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

usr        = "ubuntu"          # Username for database
database   = "printers"        # Name of database
printTable = "printers"        # Name of table for printers
errorTable = "errors"          # Name of table for errors


## Given a printer id printID and any other data about a printer, updates the corresponding printer record
## Forces an update if force is true; otherwise, depends on whether an error is set; if not, the record is updated. if so,
## the record is only allowed to update if the current time minus the time it was last updated is larger than minTime
def updatePrinter(printID, force = 0, status = None, latitude = None, longitude = None, 
	altitude = None, buildingName = None, roomNumber = None):
	
	update = force
	# Query error table for errors with this printer that are not cleared; if not, set update to true

	# Error reported for printer - compare timestamps
	#if !update:

	if update: 

		if status != None:
			updateRecord(printTable, "status", status, "printID", printID)

		if latitude != None:

			updateRecord(printTable, "latitude", latitude, "printID", printID)

		if longitude != None:
			updateRecord(printTable, "longitude", longitude, "printID", printID)

		if altitude!= None:
			updateRecord(printTable, "altitude", altitude, "printID", printID)

		if buildingName != None:
			updateRecord(printTable, "buildingName", buildingName, "printID", printID)

		if roomNumber != None:
			updateRecord(printTable, "roomNumber", roomNumber, "printID", printID)

## Updates the value of column in table for the with an identifier column that has the value idVal
## All SQL updating should happen through this function. 
## If the specified field does not exist, creates a row for it.
## Note that usage of %s in python causes automatic escaping
def updateRecord(table, column, value, identifier, idVal):
	cnx    = mysql.connector.connect(user=usr, database=database)
	cursor = cnx.cursor()
	data   = (table, identifier, idVal)

	# check if the key with identifier=idVal is in the table; if not, it needs to be inserted
	cmd  = "SELECT 1 FROM %s WHERE %s=%s"

	# record exists
	if (cursor.execute(cmd), data):
		cmd  = "UPDATE %s SET %s=%s WHERE %s=%s"
		data = (table, column, value, identifier, idVal)

	# record does not exist
	else:
		cmd  = "INSERT INTO %s (%s, %s) VALUES (%s, %s)"
		data = (table, identifier, column, idVal, value)
	
	cursor.execute(cmd, data)
	cnx.commit()
	cursor.close()
	cnx.close()
