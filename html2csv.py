#!/usr/bin/env python
#Richard's html2csv converter
#rbarnes@umn.edu

from BeautifulSoup import BeautifulSoup
import sys
import csv

if len(sys.argv)==1:
  print "Syntax: %s <HTML FILE>"
  print "Reads in an HTML and attempts to convert all tables into"
  print "CSV files."
  sys.exit(-1)

print "Opening file"
fin  = open(sys.argv[1],'r').read()

print "Parsing file"
soup = BeautifulSoup(fin,convertEntities=BeautifulSoup.HTML_ENTITIES)

print "Preemptively removing unnecessary tags"
[s.extract() for s in soup('script')]

print "CSVing file"
tablecount = -1
for table in soup.findAll("table"):
  tablecount += 1
  print "Processing Table #%d" % (tablecount)
  with open(sys.argv[1]+str(tablecount)+'.csv', 'wb') as csvfile:
    fout = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in table.findAll('tr'):
      cols = row.findAll(['td','th'])
      if cols:
        cols = [x.text for x in cols]
        fout.writerow(cols)