#!/usr/bin/env python

# from os import write
import re
from datetime import datetime, timedelta

# intializing .txt file with a list of markers
mrk = open('markers.txt')
mrk = mrk.read()
# print(mrk)

# intializing .fcpxml file with at least 1 marker
fcpx = open('import.fcpxml')
fcpx = fcpx.read()

# moving non digit character on the previous line
find = r'\n(^\D+?$)'
repl = ' \\1'
mrk0 = re.sub(find, repl, mrk, flags=re.MULTILINE) 
# print(mrk0)

# moving text from before the timecode to after the timecode
find = r'(^\D+?) (\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2})(.*)'
repl = '\\2 \\1\\3'
mrk2 = re.sub(find, repl, mrk0, flags=re.MULTILINE) 
# print(mrk2)

# puting 00 hours in where hours ar lacking
find0 = r'(^|\n| )(\d{1,2}:\d{1,2})( .*)'
repl0 = '\g<1>00:\\2\\3'
mrk1 = re.sub(find0, repl0, mrk2, flags=re.MULTILINE) 
# print(mrk1)

# converting %H:%M:%S to total seconds
find8 = r'(\d{1,2}:\d{1,2}:\d{1,2})'
def repl8_converted_to_seconds(timestamp):
    timestamp = timestamp.group()
    dt = datetime.strptime(timestamp, '%H:%M:%S')
    delta = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    return str(delta.seconds)
mrk3 = re.sub(find8, repl8_converted_to_seconds, mrk1)
# print(mrk3)

#pulling first instance of <marker> line
find10 = r'.*?<marker.*?>'
str11 = re.search(find10, fcpx) 
str12 = str11.group()
# print(str12)

#assigns varibles to <marker> syntax
find11 = r'(.*start=").*?(".*value=").*?(".*)'
repl11 = '\\1'
repl12 = '\\2'
repl13 = '\\3'
str13 = re.sub(find11, repl11, str12)
str14 = re.sub(find11, repl12, str12)
str15 = re.sub(find11, repl13, str12)
# print(str13)


#assemblying marker lines
find12 = r'(^\d*) (.*)'
repl14 = str13 + '\\1' + str14 + '\\2' + str15
str16 = re.sub(find12, repl14, mrk3, flags=re.MULTILINE)
# print(str16)

#assemblying fcpxml code
find13 = r'(^\s*<marker.*$)'
repl15 = str16 + '\n\\1'
str17 = re.sub(find13, repl15, fcpx, 1, flags=re.MULTILINE)
# print(str17)

# print(y)
with open('export.fcpxml', 'w') as f:
    f.write(str17)