
from datetime import date, datetime, timedelta

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")

from printers.models import Printer

from cgi import escape

## Given a printer buildingName, roomNumber, and any other data about a printer, updates the corresponding printer record
## Forces an update if force is true; otherwise, depends on whether an error is set; if not, the record is updated. if so,
## the record is only allowed to update if the current time minus the time it was last updated is larger than minTime
def updatePrinter(buildingName, roomNumber, force = 0, status = None, latitude = None, longitude = None, statusMsg = None,   altitude = None):

   update = force
   locVal = (buildingName, roomNumber)
   loc    = ("buildingName", "roomNumber")
   # Query error table for errors with this printer that are not cleared; if not, set update to true

   # Error reported for printer - compare timestamps
   #if !update:

   update = 1
   if update:
         try:
            p = Printer.objects.get(buildingName=buildingName, roomNumber=roomNumber)
         except Printer.DoesNotExist:
            p = Printer(buildingName=buildingName, roomNumber=roomNumber)

         if status != None:
            p.status = escape(status)

         if statusMsg != None:
            p.statusMsg = escape(statusMsg)

         if latitude != None:
            p.latitude = escape(latitude)

         if longitude != None:
            p.longitude = escape(longitude)

         p.save()
