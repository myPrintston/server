
# requires installation
import mechanize
import bs4
from bs4 import BeautifulSoup

# ------------------------------------------------------------------------
#                                Settings
# ------------------------------------------------------------------------
# delay in seconds
delay = 600

# number of times you want it to query - for debugging; uncomment 
# "for i in range(0, iterations"), comment "while (true):" to use
iterations = 2

# number of iterations between each "canDelete" operation 
#(somewhat expensively checks for and deletes no longer existent printers)
delIterations = 6

# accessing URL (specific)
url = 'http://clusters-lamp.princeton.edu/cgi-bin/clusterinfo.pl?kml=y'

# ------------------------------------------------------------------------

# already built into Python
import sys
import os
import urllib2
import re
import string

from decimal import Decimal
from time import sleep
from dbQuery import setPrinters

# custom indents - for debugging
# orig_prettify = bs4.BeautifulSoup.prettify
# r = re.compile(r'^(\s*)', re.MULTILINE)
# def prettify(self, encoding=None, formatter="minimal", indent_width=4):
#     return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
# bs4.BeautifulSoup.prettify = prettify



# sets up browser
br = mechanize.Browser()
br.set_handle_refresh(False)

building_re = re.compile('Building:.*')
room_re = re.compile('Room:.*')
printinfo_re = re.compile('Printer\(s\):.*')

latitude_re = re.compile(',.+,0</coordinates>')
longitude_re = re.compile('<coordinates>.*\d\d\.')

color_re = re.compile("'.*'")
status_re = re.compile('>.*<')
all_colors = ['#00aa00', '#ccbb00', '#dd0000']

#for i in range(0, iterations):

# Current iteration; initially, cause no longer existent printers
# to be removed at script startup 
curIter = delIterations
while (True):
    print ("running")

    buildings = []
    rooms = []
    num_printers = []
    colors = []
    statuses = []
    latitudes = []
    longitudes = []
    br.open(url)

    soup = BeautifulSoup(br.response().read())

    placemark_tags = soup.find_all('placemark')
    coordinate_tags = soup.find_all('coordinates')


    for pm in placemark_tags:
        pm_str = str(pm)

        # building

        building_raw_list = building_re.findall(pm_str)
        for bldg_raw in building_raw_list:
            # print bldg_raw
            building = bldg_raw[len("building: "):len(bldg_raw) - len("<br>")]
            # print building
            buildings.append(building)

        # room
        room_raw_list = room_re.findall(pm_str)
        for room_raw in room_raw_list:
            room = room_raw[len("Room: "):len(room_raw) - len("<br>")]
            rooms.append(room)

        printinfo_raw_list = printinfo_re.findall(pm_str)
        all_printer_re = re.compile("<font color=.*</font>")
        for printinfo_raw in printinfo_raw_list:

            colors_str = []
            colors_int = []
            indiv_statuses = []

            printinfo_raw_s2 = printinfo_raw[len("Printer(s): "):]

            # number of printers
            num_printer = int(printinfo_raw_s2[0])
            num_printers.append(num_printer)

            # indiv printers
            all_printer_list = all_printer_re.findall(printinfo_raw_s2)
            indiv_printer_list = all_printer_list[0].split('|')


            for indiv_printer in indiv_printer_list:

                # str rep of color
                colors_str_raw = color_re.findall(indiv_printer)
                color_str = colors_str_raw[0].lstrip("'").rstrip("'")

                colors_str.append(color_str)

                if all_colors.count(color_str) == 0:
                    color_int = 1
                else:
                    color_int = all_colors.index(color_str)

                # int rep of color

                colors_int.append(color_int)

                statuses_str_raw = status_re.findall(indiv_printer)
                status_str_raw = statuses_str_raw[0]
                status_str = status_str_raw.lstrip('>').rstrip('<')

                indiv_statuses.append(status_str)

            best_int = min(colors_int)
            best_status = indiv_statuses[colors_int.index(best_int)]

            colors.append(best_int)
            statuses.append(best_status)

        # print '--------------------'


    for crd in coordinate_tags:
        crd_str = str(crd)

        latitude_raw_list = latitude_re.findall(crd_str)
        longitude_raw_list = longitude_re.findall(crd_str)

        for latitude_raw in latitude_raw_list:
            latitude_str = latitude_raw.lstrip(',')[:len(latitude_raw) - len(',0</coordinates>')].rstrip(',')
            latitude = Decimal(latitude_str)
            latitudes.append(latitude)
            # print 'Latitude: ', str(latitude)

        for longitude_raw in longitude_raw_list:
            longitude_str = re.sub(re.compile(',\d\d\.'), '', longitude_raw)[len('<coordinates>'):]

            longitude = Decimal(longitude_str)
            longitudes.append(longitude)
            # print 'Longitude: ', str(longitude)

#    for i in range(0, len(buildings)):
        # print 'Building:'.ljust(19), buildings[i]
        # print 'Room:'.ljust(19), rooms[i]
        # print 'Number of printers:'.ljust(19), num_printers[i]
        # print 'Color:'.ljust(19), colors[i]
        # print 'Status:'.ljust(19), statuses[i]
        # print 'Longitude:'.ljust(19), longitudes[i]
        # print 'Latitude:'.ljust(19), latitudes[i]

        # print '--------------------'

    canDelete = 0

    if (curIter == delIterations):
        curIter = 0
        canDelete = 1

    setPrinters(canDelete = canDelete, buildings = buildings, rooms = rooms, statuses = colors, latitudes = latitudes, longitudes = longitudes, statusMsgs = statuses)  
    curIter += 1
    sleep(delay)
    # # coordinates - separated into latitude, longitude
    # bldg name
    # rm number #
    # printer status msg
    # number - color
    # G = 0, Y = 1, R = 2
