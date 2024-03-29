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
    ROWSIZE = 3

    def __init__(self):
        if (not os.path.exists(DataStorage.SAVEFILE)):
            f = tables.open_file(DataStorage.SAVEFILE, 'w')
            self.atom = tables.Int64Atom()
            local_data = f.create_earray(f.root, 'local', self.atom, (0, DataStorage.ROWSIZE))
            f.close()
        
    ## @brief Inserts the given data into a SQL Server database
    #  @param timestamp Current time data was sent
    #  @param temp Temperature reading
    #  @param humidity Humidity reading
    def SQL_insert(self, timestamp: int, temp: int, humidity: int):
        cnxn = pyodbc.connect(DataStorage.cnxn_string)
        cursor = cnxn.cursor()
        query = 'INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)' % (timestamp, temp, humidity)
        cursor.execute(query)
        cnxn.commit()

    ## @brief Stores data into a locally saved file
    #  @param timestamp Current time data was sent
    #  @param temp Temperature reading
    #  @param humidity Humidity reading
    def offline_save(self, timestamp: int, temp: int, humidity: int):
        print('Dumping to local file')

        f = tables.open_file(DataStorage.SAVEFILE, mode='a')
        sensor_data = np.array([[timestamp, temp, humidity]])
        f.root.local.append(sensor_data)
        f.close()
        
    ## @brief Syncs locally saved data with the SQL Server database
    def data_sync(self):
        print('Syncing data')

        if (os.path.exists(DataStorage.SAVEFILE)):
            f = tables.open_file(DataStorage.SAVEFILE, mode='r')
            sync_data = f.root.local[:]
            f.close()

        # Insert each locally stored array into SQL
        for i in range(len(sync_data)):
            print(i)
            cnxn = pyodbc.connect(DataStorage.cnxn_string)
            cursor = cnxn.cursor()
            print(sync_data[i])
            query = 'INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)' % (sync_data[i][0], sync_data[i][1], sync_data[i][2])
            cursor.execute(query)
            cnxn.commit()

        os.remove(DataStorage.SAVEFILE)