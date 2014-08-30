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

maxDelay = 72000  # Maximum time, in seconds, that a printer can be delayed

# Sets the set of all printers to be exactly the set contained in the printers with the given criterio
def setPrinters(canDelete, buildings, rooms, statuses, latitudes, longitudes, statusMsgs):
        # Verify that the length of all arrays passed in is the same; if not, abort
        if (len(buildings) != len(rooms) or len(rooms) != len(statuses) or len(statuses) != len(latitudes) or len(latitudes) != len(longitudes) or len(longitudes) != len(statusMsgs)):
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
        roomNubmer   = escape(roomNumber)

        try:
                p = Printer.objects.get(buildingName=buildingName, roomNumber=roomNumber)

        #printer does not exist; always update
        except Printer.DoesNotExist:
                p = Printer(buildingName=buildingName, roomNumber=roomNumber)
                update = 1

        # No errors associated with this printer; update
        if (getErrors(buildingName=buildingName, roomNumber=roomNumber, resolved=0) == serializers.serialize("json", "[]")):
                update = 1

        update = update or force

        if update:

                if status != None:
                        p.status = escape(status)

                if statusMsg != None:
                        p.statusMsg = escape(statusMsg)

                if latitude != None:
                        p.latitude = escape(latitude)

                if longitude != None:
                        p.longitude = escape(longitude)

                p.save()

# Inserts a new error with **kwargs as its values iff it does not already exist.
def insertError(resolved = 0, **kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        if (kwArgs is not None):
                try:
                        e = Errors.objects.get(resolved=resolved, **kwArgs)

                except Error.DoesNotExist:
                        e = None

                # Already reported - do not readd
                except Error.MultipleObjectsReturned:
                        return

                # Already reported - do not readd
                if (e != None):
                        return

        else:
                return

        e = Error(resolved=resolved, **kwargs)

        e.save()

        # Send email report

# When called, marks all errors with **kwargs resolved if more than maxDelay has elapsed
def autoResolveErrors(**kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        now = datetime.utcnow()

        for e in serializers.deserialize("json", getErrors(resolved=0, **kwargs)):
                if (e.object.timeUpdate != None):
                        timeDiff = now.replace(tzinfo=None) - e.object.timeUpdate.replace(tzinfo=None);
                        if (timeDiff.seconds > maxDelay):
                                e.object.resolved = 1
                                e.object.save()
                else:
                        e.object.resolved = 1
                        e.object.save()

# Returns all printers meeting criterion specified by kwargs (ie, buildingName = "B")
# would filter the printers to include only those that have a buildingName value of "B".
# By default, returns all printers.
# All values returned as jsons; returns an empty json if nothing is returned
def getPrinters(**kwargs):
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
        return serializers.serialize("json", result)

# Returns all error types meeting criterion specified by kwargs (ie, eType = "check")
# would filter the printers to include only those that with an eType value of "check"
# By default, returns all error messages
# All values returned as jsons; returns an empty json if nothing is returned
def getErrorTypes(**kwargs):
        django.db.close_connection()  # fixes MySQL timeout issues
        result = []

        # Filter the arguments based on kwargs
        if (kwargs is not None):
                try:
                        result = ErrorTypes.objects.filter(**kwargs)
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
        return serializers.serialize("json", result, fields=("eType", "eMsg", "Admin", "id"))

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
