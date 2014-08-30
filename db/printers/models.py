from django.db import models

class Printer(models.Model):
        status = models.IntegerField(null = True)      # Status of the printer (0 = working, 1 = possibly broken, 2 = broken)
        latitude = models.DecimalField(max_digits=14,decimal_places=8, null = True)   # Latitude of the printer
        longitude = models.DecimalField(max_digits=14, decimal_places=8,null = True)   # Longitude of the printer
        timeUpdate = models.DateTimeField(auto_now = True)   # Time the printer status was last updated
        buildingName = models.CharField(max_length=255)      # Name of the building the printer is in
        roomNumber = models.CharField(max_length=255)        # Room the printer is in
        statusMsg = models.CharField(max_length=255)         # Status message associated with the printer (ie, low on toner, up and running, etc)
        errorIdsReported  = models.CharField(max_length=255)  # ids (from the errorTypes page)
        activeErrorCount  = models.IntegerField()             # Number of errors that have been reported and are not resolved
        emailReportSent   = models.NullBooleanField()         # Has an email report been sent recently for reporting this printer's errors?
        jamsToday         = models.IntegerField()             # Number of jams in the last 24 hours
        lastJamReportTime = models.DateTimeField()            # Last time a jam was reported

class Error(models.Model):
        eMsg = models.CharField(max_length = 512)             # The message of the error
        comment = models.CharField(max_length = 4096)         # Any comments regarding the error
        resolved = models.NullBooleanField()                  # Is the error resolved?
        resolvedBy = models.CharField(max_length = 255)       # Who was the error resolved by?
        reporter = models.CharField(max_length = 255)         # Who reported the error?
        buildingName = models.CharField(max_length = 255)     # BuildingName of the affected printer
        roomNumber = models.CharField(max_length = 255)       # Room number of the affected printer
        timeUpdate = models.DateTimeField(auto_now = True)    # Time the error status was last updated
        timeInserted = models.DateTimeField(auto_now_add = True) # Time this error was created
        errorIdsReported = models.CharField(max_length=255)      # ErrorType ids that were reported with this error

class ErrorTypes(models.Model):
        eType = models.CharField(max_length = 32)           # Type of the error (text or check; text requires a comment to be entered in on the app side)
        eMsg  = models.CharField(max_length = 255)          # Error message for this type of error (ie "toner is low")
        weekEndEmail   = models.CharField(max_length = 255) # Who to send the emails to if this error is reported on a weekend
        weekNightEmail = models.CharField(max_length = 255) # Who to send the emails to if this error is reported on a week night
        weekDayEmail   = models.CharField(max_length = 255) # Who to send the emails to if this error is reported during a weekday
        admin          = models.BooleanField()              # Does the user need to be an admin to see the error?
        inactive       = models.BooleanField()              # Should the error be displayed on the app?

