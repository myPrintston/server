#------------------------------------------------------------------#
# File: errorTypeQueries.py                                        #
#                                                                  #
# Author: Doug Ashley (daashley@princeton.edu)                     #
#                                                                  #
# Description: Provides functions to interface with the errorType  #
# model, for both updating and retrieving errorTypes. Additional   #
# functions exist for concatenating all errorType messages from a  #
# dictionary into one, and getting the email associated with an    #
# error type.                                                      #
#------------------------------------------------------------------#

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

# Returns True if any of the errortypess denoted by eIndexes is an admin only
# errortype or if the input is invalid, and False otherwise
def errorTypeRequiresAdmin(eIndexes):
        if len(eIndexes) == 0:
                return ""

        for i in eIndexes:
                try:
                        i = int (i)
                        et = ErrorTypes.objects.get(id=i)
                        if et.admin:
                                return True

                # Unknown issue (ie, if for some reason i is not an int); report the error and return True
                # As the input is invalid
                except:
                        e = sys.exc_info()[0]
                        print("Error: %s" % str(e))
                        if (e.message != None):
                                print("Error message: %s" + str(e.message))
                        s = string.join(apply(traceback.format_exception, sys.exc_info()))
                        print (s)
                        return True
        return False

# Returns a json of the error type messages
def errorTypeJsonMessages(eIndexes):
        if len(eIndexes) == 0:
                return "[]"

        result = []
        for i in eIndexes:
                try:
                        i = int(i)
                        et = ErrorTypes.objects.get(id=i)
                        result.append(et)
                except:
                        e = sys.exc_info()[0]
                        print("Error: %s" % str(e))
                        if (e.message != None):
                                print("Error message: %s" + str(e.message))
                        s = string.join(apply(traceback.format_exception, sys.exc_info()))
                        print (s)
                        return "[]"

        return serializers.serialize("json",result, fields=("eType", "eMsg", "admin", "id"))



# Returns all error types meeting criterion specified by kwargs (ie, eType = "check")
# would filter the printers to include only those that with an eType value of "check"
# By default, returns all error messages
# All values returned as jsons; returns an empty json if nothing is returned
# Returns allFields if allFields is 1, or just eType, eMsg, Admin, and id otherwise
def getErrorTypes(allFields, **kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        result = []

        # Filter the arguments based on kwargs
        if (kwargs is not None):
                try:
                        result = ErrorTypes.objects.filter(inactive=0,**kwargs)
                except Printer.DoesNotExist:
                        return json.dumps(result)
                except FieldError:
                        return json.dumps(result)

        # Return every printer
        else:
                try:
                        result = ErrorTypes.objects.all()
                except Printer.DoesNotExist:
                        return json.dumps(result)

        # Compile the printers into a json
        if (allFields == 1):
                return serializers.serialize("json", result)
        else:
                return serializers.serialize("json", result, fields=("eType", "eMsg", "admin", "id"))

# Returns the email associated with errorType for the given **kwargs
def getErrorEmail(errorType, timePeriod):
        errorType = escape(errorType)
        timePeriod = escape(timePeriod)

        # Check that there is exactly one errortype
        try:
                et = ErrorTypes.objects.get(id=errorType)
        except ErrorTypes.DoesNotExist:
                return "undefined"
        except ErrorTypes.MultipleObjectsReturned:
                return "undefined"

        # return the appropriate kind of email
        if (timePeriod == "weekEnd"):
                return et.weekEndEmail
        if (timePeriod == "weekDay"):
                return et.weekDayEmail
        if (timePeriod == "weekNight"):
                return et.weekNightEmail
        return "undefined"

# Returns a string of all the errorMessages denoted by the numerical
# array eIndexes; information is pulled from the errorTypes database
def getErrorMessage(eIndexes, separator):
        if len(eIndexes) == 0:
                return ""
        msg = []

        for i in eIndexes:
                try:
                        i = int (i)
                        et = ErrorTypes.objects.get(id=i)

                # None found - log the error, but keep going with the other eIndexes
                except ErrorTypes.DoesNotExist:
                        print ("Id %s does not exist in the errorType database" % str(i))

                # Multiple objects have the same id - log the error, but continue with the other
                # eIndexes
                except ErrorTypes.MultipleObjectsReturned:
                        print ("Multiple objects returned for a unique id")

                # Unknown issue (ie, if for some reason i is not an int); report the error but continue
                # with the other eIndexes
                except:
                        e = sys.exc_info()[0]
                        print("Error: %s" % str(e))
                        if (e.message != None):
                                print("Error message: %s" + str(e.message))
                        s = string.join(apply(traceback.format_exception, sys.exc_info()))
                        print (s)

                else:
                        if et.eMsg == "Other":
                                et.eMsg = "User Reported Error"
                        msg.append(et.eMsg)

        msg = separator.join(map(str, msg))

        return msg

