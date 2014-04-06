# ======================================================================

# Before this will work, you may need to install BeautifulSoup and
# mechanize

# Mac (Terminal):
#   sudo pip install BeautifulSoup
#   sudo pip install mechanize

# Windows (Command Prompt):
#   easy_install BeautifulSoup
#   easy_install mechanize

# You may have to look up this tutorial on your own - I have no basis
# of testing it. All I know about Python module installation is from
# a quick Google search.

# ======================================================================

# One more issue, if you're running different versions of Python (mine
# is 2.7), you may have to install a different HTML parser.

# Mac (Terminal):
#   sudo pip install lxml

# Windows (Command Prompt):
#   easy_install lxml

# See http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
# for more details.

# ======================================================================

# MODIFICATION

# Delay can be changed in the first line of main(). I included functions
# just in case we want to modify functionality later.

# ======================================================================


# ======================================================================

# SETTINGS CAN BE MODIFIED HERE

# delay in seconds
delay = 5

# number of times you want it to query
iterations = 1

# ======================================================================

# needs installation
import mechanize
from bs4 import BeautifulSoup

import db


# already built into Python
import sys
import os
import urllib2
import re
from time import sleep

# sets up browser
br = mechanize.Browser()
br.set_handle_refresh(False)

# ======================================================================

# url for the printer data
url = 'http://clusters-lamp.princeton.edu/cgi-bin/clusterinfo.pl'

for i in range(0, iterations):
    # response = urllib2.urlopen(url)
    # html = response.read()
    # print html
    br.open(url)

    soup = BeautifulSoup(br.response().read())

# ======================================================================

    # this is excellent for debugging - you can read everything.
    # not the best for scraping though, so I'll just leave it here
    # for general interest

    # print soup.get_text()

# ======================================================================

    buildings = []
    rooms = []
    statuses = []

    first_row = True

    for row in soup.findAll("tr"):

        # We don't need the header of the table
        if first_row:
            first_row = False
            continue

        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if len(cells) == 4:
            # did I mention how great get_text() was
            building = cells[1].get_text()
            room = cells[2].get_text()
            status = cells[3].get_text()

            buildings.append(building)
            rooms.append(room)
            statuses.append(status)

    for i in range(0, len(buildings)):
        updatePrinter(buildings[i], rooms[i], force=0, status=statuses[i])
        print 'Location:', buildings[i], '-', rooms[i]
        print 'Status:', statuses[i]
    print_line()
    sleep(delay)






