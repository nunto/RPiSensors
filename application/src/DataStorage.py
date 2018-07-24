import pyodbc
import datetime
import pickle
import os
import h5py
import numpy as np
import tables

class DataStorage:
    # Connection strings
    dsn = 'sqlserverdatasource'
    db = 'SensorReadings'
    uid = 'root_sensor'
    pwd = 'Sensorread1'
    cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)
    SAVEFILE = 'localdatastore.h5'
    ROWSIZE = 8

    def __init__(self):
        #if this file does not exist
        if (not os.path.exists(DataStorage.SAVEFILE)):
            #crete a file for DataStroage and add the table settings to it
            f = tables.open_file(DataStorage.SAVEFILE, 'w')
            self.atom = tables.Int64Atom()
            local_data = f.create_earray(f.root, 'local', self.atom, (0, DataStorage.ROWSIZE))
            f.close()
        
    ## @brief Inserts the given data into a SQL Server database
    
    #  @param connection_string Connection string based on the connection details that the user put in 
    #  @param sensortype The type of sensor that sent that data
    #  @param timestamp Current time data was sent
    #  @param temp Temperature reading in degrees Celsius
    #  @param humidity Humidity reading as a percentage
    #  @param rpm The rpm as calculated based on the time between IR beam breaks
    #  @param amperage Current reading in amps
    #  @param pressure Pressure reading in PSI
    #  @param flow Flow reading in cm3 
    def SQL_insert(self, connection_string:str, tablename:str, sensortype: str, timestamp: int, temp: float, humidity: int, rpm: float, amperage: float, pressure: float, flow: float):
        cnxn = pyodbc.connect(connection_string)
        #print("Temp: " + str(temp) + "\nHumidity: " + str(humidity) + "\nrpm: " + str(rpm) + "\namperage: " + str(amperage) + "\npressure: " + str(pressure) + "\nflow: " + str(flow))
        cursor = cnxn.cursor()
        query = 'INSERT INTO ' + tablename + '(SensorID, Timestamp, Temperature, Humidity, RPM, Amperage, Pressure, Flow) values ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(sensortype, timestamp, temp, humidity, rpm, amperage, pressure, flow)
        cursor.execute(query)
        cnxn.commit()

    ## @brief Stores data into a locally saved file
    
    #  @param sensortype The type of sensor that sent that data
    #  @param timestamp Current time data was sent
    #  @param temp Temperature reading in degrees Celsius
    #  @param humidity Humidity reading as a percentage
    #  @param rpm The rpm as calculated based on the time between IR beam breaks
    #  @param amperage Current reading in amps
    #  @param pressure Pressure reading in PSI
    #  @param flow Flow reading in cm3 
    def offline_save(self, sensortype: str, timestamp: int, temp: float, humidity: int, rpm: float, amperage: float, pressure: float, flow: float):
        print('Dumping to local file')

        f = tables.open_file(DataStorage.SAVEFILE, mode='a')
        sensor_data = np.array([[ sensortype, timestamp, temp, humidity, rpm, amperage, pressure, flow]])
        f.root.local.append(sensor_data)
        f.close()
        
    ## @brief Syncs locally saved data with the SQL Server database
    def data_sync(self, connection_string:str, tablename:str):
        print('Syncing data')
        if (os.path.exists(DataStorage.SAVEFILE)):
            f = tables.open_file(DataStorage.SAVEFILE, mode='r')
            sync_data = f.root.local[:]
            f.close()

        # Insert each locally stored array into SQL
        for i in range(len(sync_data)):
            #using the connection string that was inputted by the user
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            query = 'INSERT INTO ' + tablename + '(SensorType, Timestamp, Temperature, Humidity, RPM, Amperage, Pressure, Flow) values ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(sync_data[i][0], sync_data[i][1], sync_data[i][2], sync_data[i][3], sync_data[i][4], sync_data[i][5], sync_data[i][6], sync_data[i][7])
            cursor.execute(query)
            cnxn.commit()
        #delete any data that has been synced 
        os.remove(DataStorage.SAVEFILE)
