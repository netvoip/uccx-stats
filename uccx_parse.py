#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import re
import argparse
from datetime import datetime, timedelta

Timestart = datetime.now()
vars = configparser.ConfigParser()
vars.read('uccx_vars.conf')
statpath = vars['system']['statpath']
parser = argparse.ArgumentParser(description='Returns value from text file')
parser.add_argument('file', action="store", default=False)
parser.add_argument('str', action="store", default=False)
args = parser.parse_args()

Search = args.str + '='
File = open(statpath + args.file, 'r')
Text = File.read()
File.close()

Date = datetime.strptime(Text[0:26], '%Y-%m-%d %H:%M:%S.%f')
Result = 0
if Timestart - Date > timedelta(minutes=1):
    Result = -1
else:
    Result = re.search(Search + '(\d+(\.\d+)?)', Text)[1]
print(Result)