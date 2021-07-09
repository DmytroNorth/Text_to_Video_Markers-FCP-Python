#!/usr/bin/env python

from os import write
import re
from datetime import datetime, timedelta
import os.path

# intializing .txt file with a list of markers
mrk = open('markers.txt')
mrk = markers.read()

# intializing .fcpxml file with at least 1 marker
fcpx = open('import.fcpxml')
fcpx = fcp.read()

# Finding timecode and wrap with special symbols "~" and "#"
find0 = '(\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2})'
repl0 = '~\\1#'
str1 = re.sub(find0, repl0, mrk) 

#Add '00' hours
find1 = '~(\d{1,2}:\d{1,2}\#)'
repl1 = '~00:\\1'
str2 = re.sub(find1, repl1, str1) 

#Add 0 to single digit hours
find2 = '~(\d:\d{1,2}:\d{1,2}\#)'
repl2 = '~0\\1'
str3 = re.sub(find2, repl2, str2) 

#Add 0 to single digit minutes
find3 = '(~\d{1,2}:)(\d:\d{1,2}#)'
repl3 = '\g<1>0\\2'
str4 = re.sub(find3, repl3, str3) 

#Add 0 to single digit seconds
find4 = '(~\d{1,2}:\d{1,2}:)(\d#)'
repl4 = '\g<1>0\\2'
str5 = re.sub(find4, repl4, str4) 

#Find lines of text without timecode and move it to the line above
find5 = '(\D*)\n(\D*\n)'
repl5 = '\\1 \\2'
str6 = re.sub(find5, repl5, str5) 

# Find non digit characters at the beginning of the
# line and move them past the first timecode,
# while removing most of ~, # characters and separating
# timecode and text with tab
find6 = '(^\D*)(~)(\d{2}:\d{2}:\d{2})(# )(.*)'
repl6 = '\\3 \\1\\5'
str7 = re.sub(find6, repl6, str6, flags=re.MULTILINE) 

#Remove remaining ~, # symbols
find7 = '~|#'
repl7 = ''
str8 = re.sub(find7, repl7, str7) 

# converting %H:%M:%S to total seconds
find8 = r'(\d{2}:\d{2}:\d{2})'

def repl8_converted_to_seconds(timestamp):
    timestamp = timestamp.group()
    dt = datetime.strptime(timestamp, '%H:%M:%S')
    delta = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    return str(delta.seconds)

str9 = re.sub(find8, repl8_converted_to_seconds, str8)

#pull first instance of <marker> line
find10 = '<marker.*?>'
str11 = re.search(find10, fcpx) 
str12 = str11.group()

#assigns varibles to <marker> syntax
find11 = '(.*start=").*?(".*value=").*?(".*)'
repl11 = '\\1'
repl12 = '\\2'
repl13 = '\\3'
str13 = re.sub(find11, repl11, str12)
str14 = re.sub(find11, repl12, str12)
str15 = re.sub(find11, repl13, str12)

#assemblying fcpxml code
find12 = '(^\d*) (.*)'
repl14 = str13 + '\\1' + str14 + '\\2' + str15
str16 = re.sub(find12, repl14, str9, flags=re.MULTILINE)

#assemblying fcpxml code
find13 = '(^\s*<marker.*$)'
repl15 = str16 + '\n\\1'
str17 = re.sub(find13, repl15, fcpx, 1, flags=re.MULTILINE)

# print(y)
with open('export.fcpxml', 'w') as f:
    f.write(str17)