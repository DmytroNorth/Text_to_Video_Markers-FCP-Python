# !/usr/bin/env python3

import re
import os
from datetime import datetime, timedelta

# intializing .txt file with a list of markers
inputtxt = 'videomarkers.txt'
txtpath = os.path.join(os.path.dirname(__file__), inputtxt)
mrk = open(txtpath).read()

# intializing .fcpxml file with at least 1 marker
inputxml = 'clip.fcpxml'
xmlpath = os.path.join(os.path.dirname(__file__), inputxml)
fcp = open(xmlpath).read()

# moving lines without timecode to a previous line
pat1 = r'\n(^\D+?$)'
repl1 = ' \\1'
mrk1 = re.sub(pat1, repl1, mrk, flags=re.MULTILINE)

# moving text from before the timecode to after the timecode
pat2 = r'(^\D+?) (\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2})(.*)'
repl2 = '\\2 \\1\\3'
mrk2 = re.sub(pat2, repl2, mrk1, flags=re.MULTILINE)

# puting '00:' hours in where hours are missing
pat3 = r'(^|\n| )(\d{1,2}:\d{1,2})( .*)'
repl3 = '\g<1>00:\\2\\3'
mrk3 = re.sub(pat3, repl3, mrk2, flags=re.MULTILINE)

# converting %H:%M:%S to total seconds
pat4 = r'(\d{1,2}:\d{1,2}:\d{1,2})'


def str_to_sec(tc):
    # convert re.Match class to string
    tc = tc.group()
    # convert string to datetime
    dt = datetime.strptime(tc, '%H:%M:%S')
    # convert datetime to timedelta
    td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    # calculate total seconds and convert to string
    return str(td.seconds)


mrk4 = re.sub(pat4, str_to_sec, mrk3)

# pulling first instance of <marker> line from fcpxml
pat5 = r'.*?<marker.*?>'
fcp1 = re.search(pat5, fcp)
fcp1 = fcp1.group()

# assigning varibles to <marker> parts of syntax
pat6 = r'(.*start=").*?(".*value=").*?(".*)'
repl5 = '\\1'
repl6 = '\\2'
repl7 = '\\3'
fcp2 = re.sub(pat6, repl5, fcp1)
fcp3 = re.sub(pat6, repl6, fcp1)
fcp4 = re.sub(pat6, repl7, fcp1)

# assemblying new marker lines
pat7 = r'(^\d*) (.*)'
repl8 = fcp2 + '\\1' + fcp3 + '\\2' + fcp4
fcp5 = re.sub(pat7, repl8, mrk4, flags=re.MULTILINE)

# assemblying fcpxml code
pat8 = r'(^\s*<marker.*$)'
repl8 = fcp5 + '\n\\1'
fcp6 = re.sub(pat8, repl8, fcp, 1, flags=re.MULTILINE)

# writing to a new .fcpxml file
xml2 = os.path.join(os.path.dirname(__file__), 'export.fcpxml')
with open(xml2, 'w') as newfile:
    newfile.write(fcp6)
