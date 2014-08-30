
import datetime
import pytz
import mandrill
from db.myprintstonsettings import *

# Returns the following:
# "weekEnd" if the current day is the weekend
# "weekNight" if it is after night time on a weekday
# "weekDaytime" if it is the daytime of a weekday
def getTimePeriod():
    # Set the timezone
    tz = pytz.timezone('America/New_York')

    today = datetime.datetime.today().weekday()

    # Check for if today is a weekend
    # 5 represents Saturday in weekday, 6 represents Sunday, 0 represents Monday
    if (today >= 5):
        return "weekEnd"

    # Weekday; check if it is night
    else:
        currentHour = datetime.datetime.now(tz).hour
        if (currentHour < dayStartTime or currentHour > dayEndTime):
            return "weekNight"
        return "weekDay"

    return "undefined"

# Sends an email via mandrill to mailTo with subject subject and body message
def sendEmail(mailTo, subject, message):
    try:
        mandrill_client = mandrill.Mandrill(mandrillKey)
        msg = {'from_email': mailFrom,
         'from_name': 'MyPrintsTon',
         'html': message,
         'recipient_metadata': [{'rcpt': mailTo}],
         'subject': subject,
         'text': message,
         'to': [{'email': mailTo,
                 'type': 'to'}]}
        result = mandrill_client.messages.send(message=msg, async=False)
#       print (result)
#	print (mailTo)
#        print (subject)
#        print (message)

    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        raise

