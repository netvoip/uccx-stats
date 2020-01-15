Informix ODBC seems to have versatile behavior and may vary on driver version and system setup. This article will give you an example as reference point.  
*Environment*: Ubuntu 18.04 x64, SDK 4.50.FC3.

- Get Informix Client SDK from IBM site and install it. Let's assume installation path is /opt/IBM/informix.
- Install packages `apt install unixodbc-dev unixodbc-dev` and python module `pip3 install pyodbc`
- Check ODBC configuration files location with `odbcinst -j` command.
``` 
unixODBC 2.3.4
DRIVERS............: /etc/odbcinst.ini  
SYSTEM DATA SOURCES: /etc/odbc.ini
FILE DATA SOURCES..: /etc/ODBCDataSources
USER DATA SOURCES..: /root/.odbc.ini
```  
Look at DRIVERS and SYSTEM DATA SOURCES variables. We will register drivers systemwide but you can use file DSN as well.

/etc/odbc.ini
```
[ODBC Data Sources]
uccx
uccx2

[uccx]
DRIVER={IBM INFORMIX ODBC DRIVER (64-bit)}
UID=uccxhruser
PWD=yourpassword
DATABASE=db_cra
HOST=uccx
SERVER=uccx_uccx
SERVICE=1504
PROTOCOL=onsoctcp
CLIENT_LOCALE=en_US.UTF8
DB_LOCALE=en_US.UTF8

[uccx2]
DRIVER={IBM INFORMIX ODBC DRIVER 2 (64-bit)}
UID=uccxhruser
PWD=password
DATABASE=db_cra
HOST=uccx2
SERVER=uccx2_uccx
SERVICE=1504
PROTOCOL=onsoctcp
CLIENT_LOCALE=en_US.UTF8
DB_LOCALE=en_US.UTF8
```

/etc/odbcinst.ini
```
[IBM INFORMIX ODBC DRIVER (64-bit)]
Driver=/opt/IBM/informix/lib/cli/iclis09b.so
Description=IBM INFORMIX ODBC DRIVER
UID=uccxhruser
PWD=yourpassword
DATABASE=db_cra
HOST=uccx
SERVER=uccx_uccx
SERVICE=1504
PROTOCOL=onsoctcp
CLIENT_LOCALE=en_US.UTF8
DB_LOCALE=en_US.UTF8

[IBM INFORMIX ODBC DRIVER 2 (64-bit)]
Driver=/opt/IBM/informix/lib/cli/iclis09b.so
Description=IBM INFORMIX ODBC DRIVER
UID=uccxhruser
PWD=yourpassword
DATABASE=db_cra
HOST=uccx2
SERVER=uccx2_uccx
SERVICE=1504
PROTOCOL=onsoctcp
CLIENT_LOCALE=en_US.UTF8
DB_LOCALE=en_US.UTF8
```

Also sqlhosts definition might be reqired at /opt/IBM/informix/etc/sqlhosts
```
uccx_uccx onsoctcp uccx 1504
uccx2_uccx onsoctcp uccx2 1504
```
Check your drivers with `odbcinst` -q -d command.  
Also it is supposed to test drivers with `isql -v uccx` command but in my case I get error even on working drivers.

- If you have error messages about libs check your lib like
```
ldd -v /opt/IBM/informix/lib/cli/iclis09b.so
```
It should not contain 'not found'. Sometimes it is required to create symlink from $INFORMIXDIR/lib/esql/somelib.so to $INFORMIXDIR/lib/cli/somelib.so.

- To run driver following environment variables must be declared:
```
export INFORMIXDIR=/opt/IBM/informix
export LD_LIBRARY_PATH=$INFORMIXDIR/lib:$INFORMIXDIR/lib/cli:$INFORMIXDIR/lib/esql
export INFORMIXSQLHOSTS=$INFORMIXDIR/etc/sqlhosts
```
You can put it to ~/.profile.

- unixODBC guide https://docs.snowflake.net/manuals/user-guide/odbc-linux.html  
- pyodbc wiki https://github.com/mkleehammer/pyodbc/wiki  
- Informix environment variables documentation https://www.ibm.com/support/knowledgecenter/SSGU8G_12.1.0/com.ibm.sqlr.doc/ids_sqr_312.htm

