
#------------------------------------------------------------------#
# File: errorQueries.py                                            #
#                                                                  #
# Author: Doug Ashley (daashley@princeton.edu)                     #
#                                                                  #
# Description: Provides functions to interface with the error      #
# model, for both updating and retrieving error information.       #
# Also included are functions to mark errors as resolved and       #
# entire printers as resolved.                                     #
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
import sys, traceback, string
from myprintstonsettings import *
from errorTypeQueries import *
from errorReports import *

# Inserts a new error with **kwargs as its values iff it does not already exist.
def insertError(eMsg, buildingName, roomNumber, reporter, errorTypes):
        django.db.close_connection()  # fixes MySQL timeout issues

        eMsg         = escape(eMsg)
        buildingName = escape(buildingName)
        roomNumber   = escape(roomNumber)
        reporter     = escape(reporter)

        try:
                e = Error.objects.get(resolved=0, eMsg=eMsg, buildingName=buildingName, roomNumber=roomNumber, reporter=reporter)

        except Error.DoesNotExist:
                e = None

        # Already reported - do not read
        except Error.MultipleObjectsReturned:
                return

        # Already reported - do not read
        if (e != None):
                return

        try:
                p = Printer.objects.get(buildingName=buildingName, roomNumber=roomNumber)

        # Printer does not exist or the criterion is not
        # sufficient to assign to a unique printer
        except Printer.DoesNotExist:
                return
        except Printer.MultipleObjectsReturned:
                return

        try:
                et = list(set(errorTypes + json.decoder.JSONDecoder().decode(p.errorIdsReported)))
        except:
                print ("No list of errors currently in printer list")
                et = errorTypes

        errorTypes = list(et)
        comment = eMsg
        eMsg = getErrorMessage(errorTypes, "; ")

        e = Error(resolved=0, eMsg=eMsg, errorIdsReported=json.dumps(errorTypes), comment=comment, buildingName=buildingName, roomNumber=roomNumber, reporter=reporter)

        e.save()

        # Send email report
        if (p.activeErrorCount >= (minErrorsToReport - 1) and ((timeElapsedFrom(p.timeUpdate) > emailTimeOut) or (p.emailReportSent is False))):

                # Concatenate all previous comments and reporters from errors affecting this printer
                # to send them all as one email
                c = []
                r = []
                try:
                        errors = Error.objects.filter(buildingName=buildingName, roomNumber=roomNumber, resolved=0)
                except Error.DoesNotExist:
                        print ("No errors for building=%s, room=%s found" % buildingName, roomNumber)
                        c = comment
                        r = reporter
                else:
                        for i in errors:
                                c.append(i.comment)
                                r.append(i.reporter)
                        c = "<br /><br />".join(map(str, c))
                        r = ", ".join(map(str, r))

                print ("Sending Email!")
                errorReport(comment=c, eMsg=eMsg, buildingName=buildingName, roomNumber=roomNumber, reporter=r, errorTypes=errorTypes)
                p.emailReportSent = 1
                p.status = STATUS_BAD
                p.statusMsg = eMsg
        elif p.activeErrorCount < minErrorsToReport:
                p.status = STATUS_PERR

        p.errorIdsReported = json.dumps(errorTypes)
        p.activeErrorCount = p.activeErrorCount + 1
        p.save()

# Returns all error messages meeting criterion specified by kwargs (ie, printerAffected = "B")
# would filter the printers to include only those that have a printerAffected value of "B".
# By default, returns all errors.
# All values returned as jsons; returns an empty json if nothing is returned
def getErrors(**kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        result = []

        # Filter the arguments based on kwargs
        if (kwargs is not None):
                try:
                        result = Error.objects.filter(**kwargs)
                except Error.DoesNotExist:
                        return json.dumps(result)
                except FieldError:
                        return json.dumps(result)

        # Return every printer
        else:
                try:
                        result = Error.objects.all()
                except Error.DoesNotExist:
                        return json.dumps(result)

        # Compile the printers into a json
        return serializers.serialize("json", result)

# Returns all error messages meeting criterion specified by kwargs (ie, printerAffected = "B")
# would filter the printers to include only those that have a printerAffected value of "B".
# By default, returns all errors.
# All values returned as jsons; returns an empty json if nothing is returned
# Only returns on copy of each error type
def getUniqueErrors(pid):
        django.db.close_connection()  # fixes MySQL timeout issues
        try:
                p = Printer.objects.get(id=pid)
                return errorTypeJsonMessages(json.decoder.JSONDecoder().decode(p.errorIdsReported))
        except:
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)
                return "[]"

        # Compile the printers into a json
        return serializers.serialize("json", result)


# When called, marks all errors with **kwargs resolved if more than maxDelay has elapsed
def autoResolveErrors(**kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues

        for e in serializers.deserialize("json", getErrors(resolved=0, **kwargs)):
                if (e.object.timeUpdate != None):
                        if (timeElapsedFrom(e.object.timeUpdate) > maxDelay):
                                e.object.resolved = 1
                                e.object.resolvedBy = "Resolved by System (Timeout exceeded)"
                                e.object.save()

# Marks all errors with the given printer as fixed
# Returns False if there was an error in fixing it; true if otherwise
def markPrinterFixed(pid):
        django.db.close_connection()  # fixes MySQL timeout issues

        # Update the printer status to resolve the errors
        try:
                p = Printer.objects.get(id=pid)
                p.activeErrorCount = 0
                p.emailReportSent  = 0
                p.errorIdsReported = []
                p.jamsToday        = 0
                p.status = STATUS_GOOD
                p.statusMsg = "Up and running"
                p.save()
        except:
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)

                return False

        # Mark all errors affecting the printer as resolved
        try:
                e = Error.objects.filter(buildingName=p.buildingName, roomNumber=p.roomNumber, resolved=0)
                for i in e:
                        i.resolved = 1
                        i.save()

        except Error.DoesNotExist:
                return True

        except:
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)

                return False

        return True

# Marks all errors with the given printer as fixed
# Returns False if there was an error in fixing it; true if otherwise
def markErrorFixed(pid, eids):
        if len(eids) <= 0:
                return False
        django.db.close_connection()  # fixes MySQL timeout issues

        try:
                p = Printer.objects.get(id=pid)
        except:
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)

                return False

        b = p.buildingName
        r = p.roomNumber

        print (b)
        print (r)

        try:
                e = Error.objects.filter(resolved=0, buildingName=b, roomNumber=r)
        except:
                e = sys.exc_info()[0]
                print("Error: %s" % str(e))
                if (e.message != None):
                        print("Error message: %s" + str(e.message))
                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                print (s)

                return False

        p.errorIdsReported = []

        for i in e:
                currErrs = json.decoder.JSONDecoder().decode(i.errorIdsReported)
                for a in eids:
                        try:
                                a = int(a)
                        except:
                                e = sys.exc_info()[0]
                                print("Error: %s" % str(e))
                                if (e.message != None):
                                        print("Error message: %s" + str(e.message))
                                s = string.join(apply(traceback.format_exception, sys.exc_info()))
                                print (s)

                                return False

                        if a in currErrs:
                                currErrs.remove(a)
                i.errorIdsReported = json.dumps(currErrs)
                p.errorIdsReported = list(set(p.errorIdsReported + currErrs))
                if len(currErrs) == 0:
                        print ("Marking resolved")
                        i.resolved = True
                i.save()

        p.statusMsg = getErrorMessage(p.errorIdsReported, "; ")

        if len(p.errorIdsReported) == 0:
                p.activeErrorCount = 0
                p.emailReportSent  = 0
                p.errorIdsReported = []
                p.jamsToday        = 0
                p.status = STATUS_GOOD
                p.statusMsg = "Up and running"

        p.save()

        return True

