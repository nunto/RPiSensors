# Sensor Readings

## Setting up the Raspberry Pi
Begin the setup by opening up a terminal window.  

Make sure python 2 is installed.
This can be checked by typing `python --version`. If it is not installed, type `sudo apt-get install python2.7`.

Install the following libraries via apt-get install:
- unixodbc
- unixodbc-dev
- freetds-dev
- freetds-bin (Useful for testing sql connection)
- tdsodbc  

eg: `sudo apt-get install unixodbc`.

Then, install the pyodbc library for python:   
`pip install pyodbc`.

Next is the configuration,

**First allow remote SQL connections**

Open SQL Server Configuration Manager:  
    1. SQL Server Configuration Manager (Local) > SQL Server Network Configuration > Protocols for SQL17 > Enable TCP/IP.  
    2. Right click TCP/IP > Properties > IP Addresses > IPALL > TCP Port > 1433  
    3. SQL Server Services > Right click SQL Server (SQL17) > Restart

**Now, back to the terminal** 

To edit the FreeTDS conf file:   
*Note: Use a text-editor of your choice for this, I'll use leafpad here for simplicity.*

```
cd /etc/freetds
sudo leafpad freetds.conf
```
In your text-editor, add in the lines: 

```
[sqlserver]
host = <ip address of server/computer running SQL Server>
port = <Port -- Should be 1433 if you configured SQL correctly>
tds version = 7.0
```

To figure out where unixODBC configuration files are, run:  
`odbcinst -j `. The files we want are 'drivers' and 'system data source'. It will usually be /etc/odbcinst.ini and /etc/odbc.ini.

We need to edit these files too. Starting with odbcinst.ini:
```
cd /etc/
sudo leafpad odbcinst.ini
```

and add the lines:

```
[FreeTDS]
Description = TDS Driver
Driver = /usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
Setup = /usr/lib/arm-linux-gnueabihf/odbc/libtdsS.so
CPTimeout =
CPReuse =
FileUsage = 1
```
*Note: Driver and Setup locations may be different. To find them on your RPi, in the terminal type:* `find / -name "libtds*"` *and look for the respective files*.

Moving onto the odbc.ini file:
```
sudo leafpad odbc.ini
```

and add the lines: 

```
[sqlserverdatasource]
Driver = FreeTDS
Description = ODBC connection to SQL Server
Trace = No
Servername = sqlserver
Database = <Your DB name>
```
