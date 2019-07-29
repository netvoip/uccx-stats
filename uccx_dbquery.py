#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyodbc
import configparser
from pprint import pprint

def dbquery(Query, Varsfile='uccx_vars.conf'):
    # Get variables
    vars = configparser.ConfigParser()
    vars.read(Varsfile)
    Driver = vars['uccx']['driver']
    DBuser = vars['uccx']['dbuser']
    DBpass = vars['uccx']['dbpass']
    Database = vars['uccx']['database']
    Host1 = vars['uccx']['uccx1']
    Server1 = vars['uccx']['server1']
    Host2 = vars['uccx']['uccx2']
    Server2 = vars['uccx']['server2']
    # Set up connection
    try:
        conn = pyodbc.connect('SERVICE=1504;PROTOCOL=onsoctcp;CLIENT_LOCALE=en_US.UTF8;DB_LOCALE=en_US.UTF8',
                            driver = Driver, uid = DBuser, pwd = DBpass, database = Database, host = Host1, server = Server1)
    except:
        conn = pyodbc.connect('SERVICE=1504;PROTOCOL=onsoctcp;CLIENT_LOCALE=en_US.UTF8;DB_LOCALE=en_US.UTF8',
                            driver = Driver, uid = DBuser, pwd = DBpass, database = Database, host = Host2, server = Server2)
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='UTF-8')
    conn.setdecoding(pyodbc.SQL_CHAR, encoding='UTF-8')
    conn.setencoding(encoding='UTF-8')
    cursor = conn.cursor()
    # Execute SQL query
    cursor.execute(Query)
    rows = cursor.fetchall()
    results = []
    results.append(rows)
    return(results[0])

if __name__ == '__main__':
    pprint(dbquery('select * from RtCSQsSummary'))