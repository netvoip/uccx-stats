#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import json
import requests
import urllib3
import pyodbc
import xmltodict
import configparser

from datetime import datetime, timedelta

urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA'

interval = 10
path = os.path.dirname(os.path.abspath( __file__ ))

# Get variables
vars = configparser.ConfigParser()
vars.read(os.path.abspath(os.path.join(path, 'uccx_vars.conf')))
driver = vars['uccx']['driver']
dbuser = vars['uccx']['dbuser']
dbpass = vars['uccx']['dbpass']
database = vars['uccx']['database']
host1 = vars['uccx']['uccx1']
server1 = vars['uccx']['server1']
host2 = vars['uccx']['uccx2']
server2 = vars['uccx']['server2']


def DbQuery(query):
    # Set up connection
    try:
        conn = pyodbc.connect('SERVICE=1504;PROTOCOL=onsoctcp;CLIENT_LOCALE=en_US.UTF8;DB_LOCALE=en_US.UTF8',
                            driver = driver, uid = dbuser, pwd = dbpass, database = database, host = host1, server = server1)
    except:
        conn = pyodbc.connect('SERVICE=1504;PROTOCOL=onsoctcp;CLIENT_LOCALE=en_US.UTF8;DB_LOCALE=en_US.UTF8',
                            driver = driver, uid = dbuser, pwd = dbpass, database = database, host = host2, server = server2)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='UTF-8')
    conn.setdecoding(pyodbc.SQL_CHAR, encoding='UTF-8')
    conn.setencoding(encoding='UTF-8')
    cursor = conn.cursor()
    # Execute SQL query
    cursor.execute(query)
    rows = cursor.fetchall()
    results = []
    results.append(rows)
    return(results[0])

def GetCsqStat():
    results = DbQuery('select * from RtCSQsSummary')
    text = str(datetime.now()) + '\n\n'
    for i in results:
        # Active agents = workingagents + talkingagents + reservedagents + availableagents
        Active = i[15] + i[16] + i[17] + i[2]
        # Ratio = callsabandoned / totalcalls
        if i[4]>0:
            Ratio = round(i[7]/i[4], 3)
        else:
            Ratio = 0
        text += '{} - loggedinagents={}\n'.format(str(i[0]), str(i[1]))
        text += '{} - availableagents={}\n'.format(str(i[0]), str(i[2]))
        text += '{} - unavailableagents={}\n'.format(str(i[0]), str(i[3]))
        text += '{} - talkingagents={}\n'.format(str(i[0]), str(i[16]))
        text += '{} - Active={}\n'.format(str(i[0]), str(Active))
        text += '{} - callswaiting={}\n'.format(str(i[0]), str(i[13]))
        text += '{} - totalcalls={}\n'.format(str(i[0]), str(i[4]))
        text += '{} - callshandled={}\n'.format(str(i[0]), str(i[6]))
        text += '{} - callsabandonded={}\n'.format(str(i[0]), str(i[7]))
        text += '{} - callsdequeued={}\n'.format(str(i[0]), str(i[8]))
        text += '{} - CallRatio={}\n'.format(str(i[0]), str(Ratio))
        text += '{} - avgtalkduration={}\n'.format(str(i[0]), str(round(i[9]/1000)))
        text += '{} - avgwaitduration={}\n'.format(str(i[0]), str(round(i[10]/1000)))
        text += '{} - longesttalkduration={}\n'.format(str(i[0]), str(round(i[11]/1000)))
        text += '{} - longestwaitduration={}\n'.format(str(i[0]), str(round(i[12]/1000)))
        text += '{} - oldestcontact={}\n'.format(str(i[0]), str(round(i[5]/1000)))
    
    with open(os.path.join(path, '_uccx_csqstats.txt'), 'w+') as file:
        file.write(text)

def GetOverall():
    results = DbQuery('select * from RtICDStatistics')
    text = str(datetime.now()) + '\n\n'
    for i in results:
        # Active agents = workingagents + talkingagents + reservedagents + availableagents
        Active = i[3] + i[4] + i[5] + i[6]
        text += '{} - Active={}\n'.format(str(i[0]), str(Active))
        text += '{} - loggedinagents={}\n'.format(str(i[0]), str(i[2]))
        text += '{} - availableagents={}\n'.format(str(i[0]), str(i[6]))
        text += '{} - unavailableagents={}\n'.format(str(i[0]), str(i[7]))
        text += '{} - totalcalls={}\n'.format(str(i[0]), str(i[8]))
        text += '{} - callswaiting={}\n'.format(str(i[0]), str(i[9]))
        text += '{} - callshandled={}\n'.format(str(i[0]), str(i[10]))
        text += '{} - callsabandoned={}\n'.format(str(i[0]), str(i[11]))
    
    with open(os.path.join(path, '_uccx_overall.txt'), 'w+') as file:
        file.write(text)


if __name__ == '__main__':
    starttime=time.time() 
    while True: 
        GetCsqStat()
        GetOverall()
        time.sleep(interval - ((time.time() - starttime) % interval))
