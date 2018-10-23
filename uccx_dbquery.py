#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyodbc
import configparser

def dbquery(Query, Varsfile='uccx_vars.conf'):
    # Get variables
    vars = configparser.ConfigParser()
    vars.read(Varsfile)
    Driver = vars['uccx']['driver']
    DBuser = vars['uccx']['dbuser']
    DBpass = vars['uccx']['dbpass']
    Database = vars['uccx']['database']
    Host = vars['uccx']['host']
    Server = vars['uccx']['server']
    # Set up connection
    conn = pyodbc.connect('SERVICE=1504;PROTOCOL=onsoctcp;CLIENT_LOCALE=en_US.UTF8;DB_LOCALE=en_US.UTF8',
                        driver = Driver, uid = DBuser, pwd = DBpass, database = Database, host = Host, server = Server)
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
