#------------------------------------------------------------------#
# File: printerQueries.py                                          #
#                                                                  #
# Author: Doug Ashley (daashley@princeton.edu)                     #
#                                                                  #
# Description: Provides functions to interface with the printer    #
# model, for both updating and retrieving printers                 #
#------------------------------------------------------------------#

from datetime import date, datetime, timedelta
import os
import django.db
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")
from django.core.exceptions import FieldError
from printers.models import Printer
from printers.models import Error
from django.utils.html import escape
from django.core import serializers
import json
import emails
import sys, traceback, string
from myprintstonsettings import *
from errorQueries import *
from errorReports import *

# Sets the set of all printers to be exactly the set contained in the printers with the given criterio
def setPrinters(canDelete, buildings, rooms, statuses, latitudes, longitudes, statusMsgs):
        # Verify that the length of all arrays passed in is the same; if not, abort
        if (len(buildings) != len(rooms) or len(rooms) != len(statuses) or len(statuses) != len(latitudes) or len(latitudes) != len(longitudes) or len(longitudes) != len(statusMsgs)):
                print ("Lengths of input dictionaries to setPrinters function are not the same")
                return

        # Delete any old printers that are no longer in the list
        delete = 0

        if (canDelete == 1):
                for p in serializers.deserialize("json", getPrinters()):
                        delete = 1
                        for i in range(0, len(buildings)):
                                if (p.object.buildingName == buildings[i] and p.object.roomNumber == rooms[i]):
                                        delete = 0
                                        break
                        if (delete == 1):
                                p.object.delete()

        # Mark all errors that have been unresolved for more than timeDelay
        # as resolved
        autoResolveErrors()

        # Update all remaining printers (also inserts new printers)
        for i in range(0, len(buildings)):
                updatePrinter(force = 0, buildingName = buildings[i], roomNumber = rooms[i], status = statuses[i], latitude = latitudes[i], longitude = longitudes[i], statusMsg = statusMsgs[i])


# Given a printer buildingName, roomNumber, and any other data about a printer, updates the corresponding printer record
# Forces an update if force is true; otherwise, depends on whether an error is set; if not, the record is updated. if so,
# the record is only allowed to update if the current time minus the time it was last updated is larger than minTime
def updatePrinter(buildingName, roomNumber, force = 0, status = None, latitude = None, longitude = None, statusMsg = None):
        django.db.close_connection()  # fixes MySQL timeout issues
        update = force

        buildingName = escape(buildingName)
        roomNumber   = escape(roomNumber)

        try:
                p = Printer.objects.get(buildingName=buildingName, roomNumber=roomNumber)

        #printer does not exist; always update
        except Printer.DoesNotExist:
                p = Printer(buildingName=buildingName, roomNumber=roomNumber, activeErrorCount = 0, emailReportSent = 0, jamsToday = 0, lastJamReportTime=datetime.now())
                update = 1
                force  = 1

        p.activeErrorCount = 0
        p.errorIdsReported = []
        # No errors associated with this printer; update
        try:
                e = Error.objects.filter(resolved=0, buildingName=buildingName, roomNumber=roomNumber)
                if e != None:
                        update = 0

                        # Set the active error count and error ids that have been reported
                        p.activeErrorCount = len(e)
                        if (p.activeErrorCount == 0):
                                p.emailReportSent = 0

                        for i in e:
                                try:
                                        p.errorIdsReported = list(set(p.errorIdsReported + json.decoder.JSONDecoder().decode(e.errorIdsReported)))
                                except:
                                        print ("")#print ("Error has no errorIds associated with it")
                        p.errorIdsReported = json.dumps(p.errorIdsReported)

                if len(e) < minErrorsToReport:
                        update = 1

        except Error.DoesNotExist:
                update = 1

        update = update or force

        if update:

                # Check to see if there is a jam; if there is, and there have been several jams today,
                # send an email report
                if timeElapsedFrom(p.lastJamReportTime) > timeToResetJam:
                        p.jamsToday = 0

                if (p.statusMsg is not escape(statusMsg)) and (string.find(string.lower(statusMsg), "jam") is not -1):
                        p.jamsToday = p.jamsToday + 1

                        if (p.jamsToday == 1):
                                p.lastJamReportTime = datetime.now()

                        if (p.jamsToday == minJamsToReport and p.emailReportSent == False):
                                sendJamReport(buildingName = p.buildingName, roomNumber = p.roomNumber)
                                p.emailReportSent = True

                if status != None:
                        p.status = escape(status)

                if statusMsg != None:
                        p.statusMsg = escape(statusMsg)

                if latitude != None:
                        p.latitude = escape(latitude)

                if longitude != None:
                        p.longitude = escape(longitude)

                p.save()

# Returns all printers meeting criterion specified by kwargs (ie, buildingName = "B")
# would filter the printers to include only those that have a buildingName value of "B".
# By default, returns all printers.
# All values returned as jsons; returns an empty json if nothing is returned
def getPrinters(fieldVal=1, **kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        result = []

        # Filter the arguments based on kwargs
        if (kwargs is not None):
                try:
                        result = Printer.objects.filter(**kwargs)
                except Printer.DoesNotExist:
                        return json.dumps(result)
                except FieldError:
                        return json.dumps(result)

        # Return every printer
        else:
                try:
                        result = Printer.objects.all()
                except Printer.DoesNotExist:
                        return json.dumps(result)

        # Compile the printers into a json
        if (fieldVal == 1):
                return serializers.serialize("json", result)
        elif (fieldVal == 2):
                return serializers.serialize("json", result, fields=("buildingName", "roomNumber", "id", "statusMsg", "status", "latitude", "longitude"))

        else:
                return serializers.serialize("json", result, fields=("statusMsg", "status", "id"))

# Returns the printer statuses from the given ids in the order they were given
def getPrinterStatuses(ids):
        printers = []
        for i in ids:
                try:
                        i = int(i)
                        printers.append(Printer.objects.get(id=i))
                except Printer.DoesNotExist:
                        return json.dumps([])
                except:
                        e = sys.exc_info()[0]
                        print("Error: %s" % str(e))
                        if (e.message != None):
                                print("Error message: %s" + str(e.message))
                        s = string.join(apply(traceback.format_exception, sys.exc_info()))
                        print (s)
        return serializers.serialize("json", printers, fields=("statusMsg", "status", "id"))

