# -*- coding: UTF-8 -*-
from decimal import *
from db.printerQueries import setPrinters
from db.errorReports import *
import decimal
import os

b = [u"Wilcox Hall", u"Frist Center", u"Frist Center", u"(Carl A.) Fields Center", u"Firestone Library", u"日本のプリンタ"]

r = ["Julian Street Library", "100 Level", "200 Level", "3rd floor", "B-4-K", "教頭"]

s = [0, 2, 2, 1, 1, 2]

sM = ["Up and running", "Low on toner", "Non Compliant Error Received", "Intervention Required", "Intervention Required", u"Low on トンネル/γφδ"]

lat = ["40.34489593", "40.34678505", "40.34678505", "40.34904900", "40.34957304", "35.012055", ]

long = ["-74.65607660", "-74.65473630", "-74.65473630", "-74.65149300",  "-74.65740649", "135.768246"]

setPrinters(1, b, r, s, lat, long, sM)

print ("\nDemo Part 1 Set up.")
print ("\t--Describe Basic Functionality, and unicode/colors \n\t--Mention that it handles same building names \n\t-- Click through to detailed view. \n\t--Show error reporting view. \n\t--Demonstrate client response for submitting an error (ie, need a comment, need an error selected). \n\t--Submit an error report. Show that the email appears, open the email. \n\t Back to the app: Reload the statuses of the printers to demonstrate updating. \n\t--Try to report a different error, but get the '20 minutes' message and explain server protections\n")
raw_input("Press Enter to Continue: ")

print("\n")

b = [u"Wilcox Hall", u"Frist Center", u"Frist Center", u"(Carl A.) Fields Center", u"Firestone Library", u"日本のプリンタ"]

r = ["Julian Street Library", "100 Level", "200 Level", "3rd floor", "B-4-K", "教頭"]

s = [0, 0, 0, 0, 0, 0]

sM = ["Up and running", "Up and running", "Up and running", "Up and running", "Up and running", u"Up and running"]


lat = ["40.34489593", "40.34678505", "40.34678505", "40.34904900", "40.34957304", "35.012055", ]

long = ["-74.65607660", "-74.65473630", "-74.65473630", "-74.65149300",  "-74.65740649", "135.768246"]

setPrinters(1, b, r, s, lat, long, sM)

print("\n\nDemo Part 2 Set Up.")
print("\t--Describe how the statuses change. \n\t--Note that the one reported as broken in part 1 did not change with the 'scraping'\n\t--Try to fix the red printer; show how it doesn't work unless you're an admin.\n\t--We'll come back to admin later")

raw_input("Press Enter to Continue: ")


b = [u"Wilcox Hall", u"Frist Center", u"Frist Center", u"(Carl A.) Fields Center", u"Firestone Library", u"Forbes Annex"]

r = ["Julian Street Library", "100 Level", "200 Level", "3rd floor", "B-4-K", "Annex"]

s = [2, 2, 2, 2, 2, 2]

sM = ["Low on Toner", "Low on Toner", "Paper Jam", "Low on Toner", "Paper Jam", "Too Far Away"]

lat = ["40.34489593", "40.34678505", "40.34678505", "40.34904900", "40.34957304", "0.0"]

long = ["-74.65607660", "-74.65473630", "-74.65473630", "-74.65149300",  "-74.65740649", "0.0"]

setPrinters(1, b, r, s, lat, long, sM)

sendJamReport("Firestone Library", "B-4-K")

print ("\n\nDemo Part 3 Set Up.")
print ("--Reload by selecting the printer detailed view and then loading the page\n\t--Email comes through for jam report. Load it, and describe how emails come through for jams. \n\t--Note how the printer was removed.\n\t--Go to map view, describe the colors and view.\n\t--Go to admin view.\n\t--Describe admin privileges\n\t--Attempt to login with incorrect user/pass\n\t--Login with correct username/pass\n\t--Go to report an error\n\t--Note the new error that shows up\n\t--Report two errors to demonstrate unlimited access\n\t--Fix a printer\n\t")
raw_input("Press Enter to Continue: ")


b = ['1901/Laughlin Hall', '1937 Hall', '1981 Hall', 'Blair Hall', 'Bloomberg Hall', 'McDonnell Hall', 'Butler Apts.', 'Butler College bldg. D', 'Campus Club', 'Center for Jewish Life', 'Dod Hall', 'Edwards Hall', '(Carl A.) Fields Center', 'Firestone Library', 'Fisher Hall (Whitman)', 'Forbes Annex', 'Forbes College', 'Forbes College', 'Foulke Hall', 'Frist Center', 'Frist Center', 'Frist Center', 'Graduate College (old)', 'Holder Hall', 'Holder Hall', 'Joline Hall', 'Lauritzen Hall', 'Lawrence Apts.', 'Lawrence Apts.', 'Little Hall', 'Little Hall', 'Madison Hall', 'McCosh Hall', 'New Graduate College', 'Pyne Hall', 'Scully Hall', 'Scully Hall', 'Spelman bldg. 5', 'Whitman North Hall', 'Wilcox Hall', 'Witherspoon Hall', 'Wright Hall', 'Wu Hall']


r = ['basement', 'ground floor', 'FB10', 'entry 11 basement', '315', 'Brush Gallery', '226f Marshall St.', '33', '2nd floor', '2nd floor', 'Printer room- lower level', 'basement', '3rd floor', 'B-4-K', 'A213', 'Annex', 'basement 014C', 'Library', '3rd entry basement', '100 level', '200 level', '300 level', 'B-9-B', 'B11', 'B31', 'Basement Lounge', 'D409', 'Building 1', 'Building 14', 'basement- north end', 'basement- south end', 'Library', 'B59', 'entry 33/34', '231', '269a', '309', 'Laundry room', 'Library', 'Julian Street Library', '109', '3rd floor by lounge', 'Mellon Library']

s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sM = ["Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running", "Up and running"]

lat = [Decimal('40.34608196'), Decimal('40.34588186'), Decimal('40.3435424'), Decimal('40.347402'), Decimal('40.343125'), Decimal('40.34535745'), Decimal('40.347766'), Decimal('40.344491'), Decimal('40.347571'), Decimal('40.34667209'), Decimal('40.34679141'), Decimal('40.34714523'), Decimal('40.349049'), Decimal('40.34957304'), Decimal('40.34472002'), Decimal('40.341655'), Decimal('40.342'), Decimal('40.3425'), Decimal('40.346332'), Decimal('40.34678505'), Decimal('40.34678505'), Decimal('40.34678505'), Decimal('40.33790879'), Decimal('40.3489'), Decimal('40.3484'), Decimal('40.347907'), Decimal('40.34365764'), Decimal('40.33235518'), Decimal('40.33350361'), Decimal('40.34656'), Decimal('40.345977'), Decimal('40.34850052'), Decimal('40.348403'), Decimal('40.340574'), Decimal('40.345235'), Decimal('40.344667'), Decimal('40.34420655'), Decimal('40.344375'), Decimal('40.34408781'), Decimal('40.34489593'), Decimal('40.34745173'), Decimal('40.3457006'), Decimal('40.3446')]

long = [Decimal('-74.66018544'), Decimal('-74.65618731'), Decimal('-74.65730257'), Decimal('-74.661934'), Decimal('-74.655858'), Decimal('-74.65248335'), Decimal('-74.638546'), Decimal('-74.65523'), Decimal('-74.654435'), Decimal('-74.65362599'), Decimal('-74.65865801'), Decimal('-74.65927882'), Decimal('-74.651493'), Decimal('-74.65740649'), Decimal('-74.65823409'), Decimal('-74.660664'), Decimal('-74.66118425'), Decimal('-74.66155'), Decimal('-74.66091611'), Decimal('-74.6547363'), Decimal('-74.6547363'), Decimal('-74.6547363'), Decimal('-74.6524486'), Decimal('-74.6615'), Decimal('-74.6613'), Decimal('-74.662011'), Decimal('-74.658338'), Decimal('-74.6565112'), Decimal('-74.65788693'), Decimal('-74.659985'), Decimal('-74.659383'), Decimal('-74.66220304'), Decimal('-74.655895'), Decimal('-74.66679'), Decimal('-74.659851'), Decimal('-74.654815'), Decimal('-74.65473139'), Decimal('-74.659312'), Decimal('-74.65824793'), Decimal('-74.6560766'), Decimal('-74.66012844'), Decimal('-74.65758709'), Decimal('-74.6564')]

setPrinters(1, b, r, s, lat, long, sM)

print ("\nDemo Part 4 Set Up")
print ("\n\t--Printer addition - lots\n\t--Admin logout")
raw_input("Press Enter to Continue")

os.system("/home/ubuntu/db/getclusterinfo.py")

