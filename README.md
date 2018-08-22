# Sensor Readings
Project Description here


## Usage  
--------
*Here is where usage info will go once the application is finished*

By default database configurations are saved, and reused. To change the configurations simply delete configuration.pickle for database configurations, and sensorconfiguration.pickle for the sensor configuration.
Table columns must be saved in DataStorage.py to properly send. 


## Setting up the Raspberry Pi for SQL
--------------------------------------
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

## Setting up the Sensors 
-------------------------

### For Data Storage

HDF5 is used for the local storage. Download the hdf5 tar.gz file (We used version 1.8.21).


Open a terminal window and navigate to the directory of the .tar.gz file:
```
tar -zxf hdf5.<X.Y.Z>.tar.gz  NOTE: replace with your filename
cd hdf5.X.Y.Z
./configure --prefix=/usr/local/hdf5
make
sudo make install

sudo apt-get update
sudo apt-get install libhdf5-dev
sudo apt-get update
sudo apt-get install libhdf5-serial-dev

cd /etc/ld.so.conf.d
sudo leafpad locallibs.conf
```
In your texteditor type: 
`/usr/local/` then save and exit

```
sudo ldconfig
python3 -m pip install h5py
python3 -m pip install tables
```

If there is a lbf77blas.so.3 error, running `sudo apt-get install libatlas-base-dev` should resolve the issue.

### GUI

PyQt5 must be installed for the gui to display.
In a terminal:
```
sudo apt-get install python3-PyQt5
```

### NTP
Ntp is used to sync the RPi clock.
In a terminal:
```
sudo apt-get install ntp 
```

### DHT 11 - Temperature and Humidity

This one should be set up as long as the DHT11.py class file is not removed from the lib folder.

### Temperature Sensor (Thermal Probe) - DS18B20

In a terminal window:  
```
python3 -m pip install w1thermsensor
sudo apt-get install python3-w1thermsensor

cd /boot
sudo leafpad config.txt
```

In the text editor, add in the line:  
`dtoverlay=w1-gpio,gpiopin=<PIN#>`  
replacing <PIN#> with the number of the pin you are using.

### Analog to Digital Convertor Chip - MCP3008
In a terminal window:
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip
sudo pip install adafruit-mcp3008
```
### Setting up on boot launching ###
In a terminal window:
```
sudo leafpad /etc/profile
```
In the text editor, add in the lines :
```
cd /home/pi/SensorProject
sudo python3 SensorMain.py
```

If for any reason booting on launch is no longer needed, it can be turned off by adding a # before sudo python3 SensorMain.py in the previous step.

If an error saying "Cannot load w1 kernel modules" occurs, rebooting the Pi should resolve the issue.
