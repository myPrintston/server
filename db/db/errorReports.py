#------------------------------------------------------------------#
# File: errorReports.py                                            #
#                                                                  #
# Author: Doug Ashley (daashley@princeton.edu)                     #
#                                                                  #
# Description: Provides error and jam reporting functionality, and #
# provides a function to calculate time elapsed between a time in  #
# past and the present time                                        #
#------------------------------------------------------------------#

from datetime import date, datetime, timedelta
import os
import django.db
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")
from django.core.exceptions import FieldError
from printers.models import Printer
from printers.models import Error
from printers.models import ErrorTypes
from django.utils.html import escape
from django.core import serializers
import json
import emails
import sys, traceback, string
from errorTypeQueries import *
from myprintstonsettings import *

# Returns the time elapsed between time and now in seconds
def timeElapsedFrom(time):
        now = datetime.utcnow()
        timeDiff = now.replace(tzinfo=None) - time.replace(tzinfo=None)
        return timeDiff.seconds

# Sends an error report
def errorReport(eMsg, reporter, buildingName, roomNumber, errorTypes, comment):
        if (len(errorTypes) == 0):
                return

        # Create the message to send
        msg = "A printer error has been reported. <br /><br />"
        msg += "<strong>Building:</strong>      %s <br /><br />" % buildingName
        msg += "<strong>Room:</strong>          %s <br /><br />" % roomNumber

        if (reporter != ""):
                msg += "<strong>Reporter Netids:</strong>          %s <br /><br />" % reporter

        msg += "<strong>Errors</strong>:       %s <br /><br />" % eMsg

        msg += "<strong>Comments:</strong>          %s <br /> <br />" % comment

        subject = "Problem in " + buildingName + " " + roomNumber;

        email = []

        timePeriod = emails.getTimePeriod()

        # Send an email to each affected party
        for i in errorTypes:
                newEmail = getErrorEmail(i, timePeriod)

                if (not newEmail in email):
                        email.append(newEmail)

        for i in email:
                if (i != "undefined" and i != None):
                        emails.sendEmail(i, subject, msg)
                else:
                        print ("Undefined Email Address")


# Sends an error report
def sendJamReport(buildingName, roomNumber):

        # Create the message to send
        msg = "The printer in <strong>%s %s</strong> has had %s jams in the last %s hours and has not been reported by users. It is recommended that the printer be investigated. <br /><br />" % (buildingName, roomNumber, str(minJamsToReport), str(timeToResetJam / 3600),)

	try:
		errorReport(eMsg = "Paper Jam", reporter = "MyPrintsTon jam report", buildingName = buildingName, roomNumber = roomNumber, errorTypes = [ErrorTypes.objects.get(eMsg = "Paper Jam").id], comment = msg)
	except:
		print ("Failure")
		
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)

                return False



