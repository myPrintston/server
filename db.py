from __future__ import print_function
from datetime import date, datetime, timedelta
import MySQLdb as mdb
import re

usr        = "ubuntu"          # Username for database
host       = "localhost"       # Host name for database
db         = "printers"        # Name of database
pw         = ""                # Password for database
printTable = "printers"        # Name of table for printers
errorTable = "errors"          # Name of table for errors
idTable    = "ids"             # Name of table for assigning ids


## Given a printer buildingName, roomNumber, and any other data about a printer, updates the corresponding printer record
## Forces an update if force is true; otherwise, depends on whether an error is set; if not, the record is updated. if so,
## the record is only allowed to update if the current time minus the time it was last updated is larger than minTime
def updatePrinter(buildingName, roomNumber, force = 0, status = None, latitude = None, longitude = None, statusMsg = None
        altitude = None):

        update = force
        locVal = (buildingName, roomNumber)
        loc    = ("buildingName", "roomNumber")
        # Query error table for errors with this printer that are not cleared; if not, set update to true

        # Error reported for printer - compare timestamps
        #if !update:

        if update:

                if status != None:
                        updateRecord(printTable, "status", status, loc, locVal)

                if statusMsg != None:
                        updateRecord(printTable, "statusMsg", statusMsg, loc, locVal)

                if latitude != None:
                        updateRecord(printTable, "latitude", latitude, loc, locVal)

                if longitude != None:
                        updateRecord(printTable, "longitude", longitude, loc, locVal)

                if altitude!= None:
                        updateRecord(printTable, "altitude", altitude, loc, locVal)

                if buildingName != None:
                        updateRecord(printTable, "buildingName", buildingName, loc, locVal)

                if roomNumber != None:
                        updateRecord(printTable, "roomNumber", roomNumber, loc, locVal)

## Updates the value of column in table for the with an identifier column that has the value idVal
## All SQL updating should happen through this function.
## If the specified field does not exist, creates a row for it.
## Excepts both tuples and strings
def updateRecord(table, columns, values, ids, idVals):
        constraints = " AND ".join('%s="%s"' % a for a in zip(ids, idVals))

        # Convert everything to a tuple for consistent processing
        columns = (columns,)
        values = (values,)
        ids = (ids,)
        idVals = (idVals,)

        # check if the key with identifier=idVal is in the table; if not, it needs to be inserted
        cmd  = "SELECT 1 FROM %s WHERE %s"
        inputs = (table, constraints)
        exists = executeSQL(cmd, inputs)

        # record does not exist; create it with the basic ids and constraints
        if (exists==None):
                cmd  = "INSERT INTO %s %s VALUES %s" % table
                a = ", ".join(map(str, ids))
                a = a.replace("'", "")
                b = ", ".join(map(str, idVals))
              #  cmd += ", ".join(map(str, ids))
              #  cmd  = cmd.replace("'", "")             # removes extra quotes from str()
               # cmd += " VALUES " + ", ".join(map(str, idVals)) + ""
                inputs = (table, a, b)
                executeSQL(cmd, inputs)

        cmd = "UPDATE %s SET %s WHERE %s"
        a = ", ".join('%s="%s"' % a for a in zip(columns, values))
        #cmd += " WHERE " + constraints
        inputs = (table, a, constraints)
        executeSQL(cmd, inputs)

## Retrieves the given column from the table, given constraints
## ids and idVals (provided as a string or tuple)
def getRecord(table, column, ids, idVals):
        constraints = " AND ".join('%s="%s"' % a for a in zip(ids, idVals))

        # Convert everything to a tuple for consistent processing
        ids = (ids,)
        idVals = (idVals,)

        # check if the key with identifier=idVal is in the table;
        # if not, return "NULL"
        cmd  = "SELECT 1 FROM %s WHERE %s"
        inputs = (table, constraints)
      #  cmd += constraints
        exists = executeSQL(cmd, inputs)

        # Nothing obtained
        if (exists == None):
                return "NULL";

        # Something exists for the given constraints; return the value from
        # the given column
        cmd  = "SELECT %s FROM %s WHERE %s" #% column
        #cmd += "%s WHERE " % table
        #cmd += constraints
        inputs = (column, table, constraints)
        return executeSQL(cmd, inputs)

## Executes the given SQL command.
def executeSQL(cmd, inputs):
        cnx    = mdb.connect(host,usr, pw,db, charset='utf8', use_unicode=true)
        cursor = cnx.cursor()
        print (cmd)
        cursor.execute(cmd, inputs)
        val = cursor.fetchone()
        cnx.commit()
        cursor.close()
        cnx.close()
        return val;