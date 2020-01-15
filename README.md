### Introduction
Set of tools to get statistics from UCCX database and parse it for further processing in wallboard and history graphs.

### Requirements
- Python 3+ with pyodbc module installed.
- IBM Informix driver as part of Informix Client SDK installed.
uccx-dsn.dsn is an example file of ODBC configuration on Windows. odbcinst.ini is an example file of ODBC configuration on Linux.
- Unix-only: unixODBC package installed and configured. See [guide](doc/ODBC_guide.md) .
- UCCX real-time data collecting enabled at "Tools -> Real Time Snapshot Writing Configuration" with both "CCX CSQs Summary" and "CCX System Summary" options.

### Usage
`uccx_getcsqstat.py` collects statistics for every existing CSQ and stores it in _uccx_csqstats.txt file.
For 30 seconds launch add two lines like these to your cron file:
```
* * * * * user . $HOME/.profile; cd /opt/uccx-stats/ && python3 uccx_getcsqstat.py > /dev/null 2>> ./uccx-stats.log
* * * * * user ( . $HOME/.profile; sleep 30; cd /opt/uccx-stats/ && python3 uccx_getcsqstat.py > /dev/null 2>> ./uccx-stats.log )
```  

`uccx_getoverall.py` collects summary statistics for all CSQs and keeps it in _uccx_overall.txt file.
For 60 seconds launch add line like this to your cron file:
```
* * * * * user ( . $HOME/.profile; sleep 10; cd /opt/uccx-stats/ && python3 uccx_getoverall.py > /dev/null 2>> ./uccx-stats.log )
```

`uccx_parse.py` extracts value from text file. Use it to fill data on your monitoring system or database directly. 
First paramter is file name, second is variable, for example:  
`python3 uccx_parse.py _uccx_csqstats.txt 'Sales_CSQ - loggedinagents'`  

Colledted items are: 
- active (= working + talking + reserved + available), 
- loggedinagents, 
- availableagents, 
- unavailableagents, 
- talkingagents, 
- callswaiting, 
- totalcalls, 
- callshandled, 
- callsabandonded, 
- callsdequeued, 
- callratio (= handled / total), 
- avgtalkduration, 
- avgwaitduration, 
- longesttalkduration, 
- longestwaitduration, 
- oldestcontact.  

For overall: 
- active, 
- loggedinagents, 
- availableagents, 
- unavailableagents, 
- totalcalls, 
- callswaiting, 
- callshandled, 
- callsabandoned.

### Example
This is what it looks like on Grafana using Zabbix datasource.  

![Wallboard example](./doc/example_wallboard.png)
