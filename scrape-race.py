#!/usr/bin/env python
"""
Grabs race results from LiveTiming into a CSV file.

Usage:

  scrape-race.py [-r <race-id>] [-f <filename>]

  -r <race-id>  Fetch the race results directly from live-timing.com
                using the specified race ID.

  -f <filename> Parse race results out of a page that's already been
                fetched from live-timing.com.
          
"""

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from getopt import GetoptError, getopt
import re
import sys

try:
    opts, args = getopt(sys.argv[1:], 'f:r:', ['file=', 'race='])
except GetoptError, e:
    print >> sys.stderr, e
    sys.exit(2)

html = None

for o, a in opts:
    if o in ('-f', '--file'):
        html = open(a, 'r')
    elif o in ('-r', '--race'):
        html = urlopen('http://live-timing.com/race.php?r=%s' % a)

if not html:
    print >> sys.stderr, "please specify '-r' or '-f'"
    sys.exit(2)

def parse_time(s):
    m = re.match(r'((?P<minutes>\d+):)?(?P<seconds>[0-9.]+)', s.strip())
    if m:
        return str(float(m.group('minutes') or '0') * 60 + float(m.group('seconds')))
    return ''

soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

th = soup.find('tr', { 'class': 'tableheader' })
cols = [ n.getText() for n in th ]
print ','.join(cols)

for tr in soup.findAll('tr', { 'class': 'table' }):
    row = dict(zip(cols, (n.getText().encode('utf8') for n in tr)))

    row['Name'] = '"%s"' % row['Name']
    row['Result 1'] = parse_time(row['Result 1'])
    row['Result 2'] = parse_time(row['Result 2'])
    row['Combined'] = parse_time(row['Combined'])

    print ','.join(row[k] for k in cols)
