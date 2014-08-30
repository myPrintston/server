#------------------------------------------------------------------#
# File: views.py                                                   #
#                                                                  #
# Author: Doug Ashley (daashley@princeton.edu)                     #
#                                                                  #
# Description: Processes url requests as directed from urls.py and # 
# behaves accordingly, returning results relevant to the request.  #
#------------------------------------------------------------------#

from django.http import *
from django.contrib.auth.decorators import login_required

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import json
import django.utils.html
import datetime
import printerQueries
import errorQueries
import errorTypeQueries
import sys, traceback, string
from myprintstonsettings import *

maxCookieAge = 1200

# Get the status of all printers, returning it with all fields
def allPrinters(request):
   return HttpResponse(printerQueries.getPrinters(fieldVal=2))

# Get the statuses of all printers, returning only the printer ids, statuses, and status messages
def allPrinterStatuses(request):
   return HttpResponse(printerQueries.getPrinters(fieldVal=0))

# Returns all the active errors associated with the printer in buildingName, roomNumber
def getErrors(request, pid):
   print ("Correct view")
   pid = escape(pid)
   try:
       pid = int(pid)
   except:
       return HttpResponse(json.dumps("[]"))
   return HttpResponse(errorQueries.getUniqueErrors(pid))

def fixErrors(request, pid, eid):
   pid = escape(pid)
   eid = escape(eid).split("/")
   if (not request.user.is_authenticated()):
      return HttpResponse(json.dumps([False, "Please login as an administrator to report an error as being fixed"]))
   else:
      try:
         pid = int(pid)
         if (errorQueries.markErrorFixed(pid, eid) == False):
            return HttpResponse(json.dumps([False,"There was an error reporting the error with eid %s as fixed" % str(eid)]))
         else:
            return HttpResponse(json.dumps([True,"Thank you for reporting the error as fixed!"]))
      except:
         e = sys.exc_info()[0]
         print("Error: %s" % str(e))
         if (e.message != None):
            print("Error message: %s" + str(e.message))
         s = string.join(apply(traceback.format_exception, sys.exc_info()))
         print (s)
         return HttpResponse(json.dumps([False,"There was an error in reporting the error with eid %s as fixed" % str(eid)]))
   return HttpResponse(json.dumps([False,"Error: unreachable code reached"]))

# Return the ids, statuses, and statusmsgs of the printers with ids specified in args, separated by '/'
def printerStatuses(request, args):
   args = escape(args).split("/")
   return HttpResponse(printerQueries.getPrinterStatuses(args))

# Return the status of the printer specified by pid, and the statusmsg
def onePrinterStatus(request, pid):
   try:
      pid = int(pid)
   except ValueError:
      pid = 0
   return HttpResponse(printerQueries.getPrinters(fieldVal=0, id=pid))

# Return all of the errortypes with fields for the app
def allErrorTypes(request):
   request.session.set_test_cookie()
   return HttpResponse(errorTypeQueries.getErrorTypes(allFields=0))

# Return true if logged in, false otherwise
def checklogin(request):
   if (not request.user.is_authenticated()):
      return HttpResponse(json.dumps([False]))
   return HttpResponse(json.dumps([True]))

# If the user is logged in, fix the printer with id pid if it exists; otherwise, return an error message
def fixPrinter(request, pid):
   if (not request.user.is_authenticated()):
      return HttpResponse(json.dumps([False, "Please login as an administrator to report a printer as being fixed"]))
   else:
      pid = escape(pid)
      try:
         pid = int(pid)
         if (errorQueries.markPrinterFixed(pid) == False):
            return HttpResponse(json.dumps([False,"There was an error reporting the printer with pid %s as fixed" % str(pid)]))
         else:
            return HttpResponse(json.dumps([True,"Thank you for reporting the printer as fixed!"]))
      except:
         e = sys.exc_info()[0]
         print("Error: %s" % str(e))
         if (e.message != None):
            print("Error message: %s" + str(e.message))
         s = string.join(apply(traceback.format_exception, sys.exc_info()))
         print (s)
         return HttpResponse(json.dumps([False,"There was an error in reporting the printer with pid %s as fixed" % str(pid)]))
   return HttpResponse(json.dumps([False,"Error: unreachable code reached"]))

# Adds an error message specified in the json stored in the POST body, after validating that the
# json is a valid json
def addError(request):
   # Method should be POST
   if request.method != "POST":
      return HttpResponse("Invalid input format")


   request.session.set_test_cookie()
   # Cookies must be enabled to store session data
   if not request.session.test_cookie_worked() and cookieCheckEnabled is True:
      request.session.set_test_cookie()
      return HttpResponse("Please enable cookies to submit an error report. ")

   print (request.session.get("has_reported"))
   print (cookieCheckEnabled)
   print (request.user.is_authenticated())
   # Only allow an error submission if no session is active
   if request.session.get("has_reported", False) and cookieCheckEnabled is True and not request.user.is_authenticated():
      return HttpResponse("Please wait %s minutes between each error report" % (maxCookieAge / 60))

   # Sanitize the input, then make sure that it is a valid JSON
   d = escape(request.body)
   try:
      d = json.loads(d)
   except ValueError, e:
      print ("Invalid input format")
      return HttpResponse("Invalid input format")

   # Check that the json object contains the desired fields
   if (keysExist(d, ("printerid", "netid", "buildingName", "roomNumber", "errors",  "errMsg")) == False):
      print ("Invalid input format")
      return HttpResponse("Invalid input format")

   # Check if the user must be logged in to report an error
   if request.user.is_authenticated() is False:
      if errorTypeQueries.errorTypeRequiresAdmin(eIndexes=d['errors']):
        print ("User attempting to report admin only error type")
        return HttpResponse("Please login as an administrator to report this type of error")

   # Insert the error
   errorQueries.insertError(eMsg=d['errMsg'], buildingName = d['buildingName'], roomNumber=d['roomNumber'], reporter=d['netid'], errorTypes=d['errors'])
   response = HttpResponse("Thank you for your report!")
   request.session["has_reported"] = True
   request.session.set_expiry(datetime.timedelta(seconds=maxCookieAge))

   return response

# Returns True if all keys exist in the jsonObj, and False otherwise
def keysExist(jsonObj, keys):
   for k in keys:
      if (not k in jsonObj):
         return False

   return True


