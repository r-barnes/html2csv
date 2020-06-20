#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Richard's html2csv converter
#rijard.barnes@gmail.com
#

from bs4 import BeautifulSoup
import argparse
import csv
import fileinput
import sys

parser = argparse.ArgumentParser(description='Reads in an HTML and attempts to convert all tables into CSV files.')
parser.add_argument('--delimiter', '-d', action='store', default=',',help="Character with which to separate CSV columns")
parser.add_argument('--quotechar', '-q', action='store', default='"',help="Character within which to nest CSV text")
parser.add_argument('filename', nargs="?", help="HTML file from which to extract tables")
args = parser.parse_args()

data = list(fileinput.input(files=(args.filename, ) if args.filename is not None else ('-', )))
data = "\n".join(data)

soup = BeautifulSoup(data, "html.parser")

#Preemptively removing unnecessary tags
[s.extract() for s in soup('script')]

for index,table in enumerate(soup.findAll("table")):
  fout = csv.writer(sys.stdout, delimiter=args.delimiter, quotechar=args.quotechar, quoting=csv.QUOTE_MINIMAL)
  for row in table.findAll('tr'):
    cols = row.findAll(['td','th'])
    if cols:
      cols = [str(x.text).strip() for x in cols]
      fout.writerow(cols)

  print("\n\n###")