### Introduction
Set of tools to get statistics from UCCX database and parse it for further processing in wallboard and history graphs.

### Requirements
- Python 3+ with pyodbc module installed.
- IBM Informix driver as part of Informix Client SDK installed.
uccx-dsn.dsn is an example file of ODBC configuration on Windows. odbcinst.ini is an example file of ODBC configuration on Linux.
- Linux-only: unixODBC package installed. Some environment variables might be required, as example:
`export INFORMIXDIR=/opt/IBM/informix
export LD_LIBRARY_PATH=$INFORMIXDIR/lib:$INFORMIXDIR/lib/cli:$INFORMIXDIR/lib/esql`
- UCCX real-time data collecting enabled at "Tools -> Real Time Snapshot Writing Configuration" with both "CCX CSQs Summary" and "CCX System Summary" options.

### Usage
`uccx_getcsqstat.py` collects statistics for every existing CSQ and keeps it in _uccx_csqstats.txt file.
For 30 seconds launch add these two lines to your cron file:
`* * * * * username . $HOME/.profile; cd /opt/uccx-stats/ && ./uccx_getcsqstat.sh > /dev/null 2>> ./uccx-stats.log
* * * * * username ( . $HOME/.profile; sleep 20; cd /opt/uccx-stats/ && ./uccx_getcsqstat.sh > /dev/null 2>> ./uccx-stats.log )`  

`uccx_getoverall.py` collects summary statistics for all CSQs and keeps it in _uccx_overall.txt file.
For 60 seconds launch add this line to your cron file:
* * * * * username ( . $HOME/.profile; sleep 10; cd /opt/uccx-stats/ && ./uccx_getoverall.sh > /dev/null 2>> ./uccx-stats.log )

`uccx_parse.py` extracts value from text file. Use it to fill data on your monitoring system or database directly. 
First paramter is file name, second is variable, for example:
`python ./uccx_parse.py _uccx_csqstats.txt 'Sales_CSQ - loggedinagents'`

### Example
This is what it looks like on Grafana connected to Zabbix.