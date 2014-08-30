
import pytz
timeZone     = pytz.timezone("America/New_York")
maxDelay     = 74400  # Maximum time, in seconds, that a printer can be delayed
STATUS_GOOD  = 0      # Printer status is fine, working well
STATUS_PERR  = 1      # Possible error with the printer
STATUS_BAD   = 2      # Known issue with the printer
emailTimeOut = 34400  # Time, in seconds, between subsequent calls for one printer experiencing errors
minErrorsToReport = 1 # Minimum number of errors for a single printer that must be reported before an email is sent
minJamsToReport   = 1 # Number of jams that must be seen before reporting a jam problem
timeToResetJam    = 86400 # Number of seconds between when a jam is first reported and when the number of jams is reset

# Emails to send automatic jam reports to
emailToReportJams = {"weekEnd": "bmwong@princeton.edu",
                     "weekNight": "bmwong@princeton.edu",
                     "weekDay": "bmwong@princeton.edu"}

maxCookieAge = 1200 # Number of seconds between error reports
cookieCheckEnabled = True # Check for whether the user has reported an error recently


# Time for start of a weekday / end of a weekday
dayStartTime = 8   # Time in hours that the weekDay should start [0-23]
dayEndTime   = 17  # Time in hours that the weekDay should end [0-23]
mailFrom     = "MyPrintsTon@princeton.edu"
mandrillKey  = "M869Z86-lP0LK0BZEJrohQ"

