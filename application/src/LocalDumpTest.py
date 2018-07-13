import pickle

"""
with open('localdatadump.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
"""    

    

"""
#make a to be the data being read everytime(as an array?)
if reading.is_valid():
    a= [current_time, reading.temperature, reading.temperature]
    with open('localdatadump.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
 """       
    
"""
In order to sync, use
with open('localdatadump.pickle', 'rb') as handle:
    b=pickle.load(handle)
"""
objects =[]
def syncfromlocal():
    global objects
    with open('localdatadump.pickle', 'rb') as handle:
        while True:
            try:
                objects.append(pickle.load(handle))
                print("Loading")
            except EOFError:
                break
    # SQL Server connection details
    dsn = 'sqlserverdatasource'
    db = 'SensorReadings'
    uid = 'root_sensor'
    pwd = 'Sensorread1'
    cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)

    # Connecting SQL Server
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()
    global current_time
    
    # Inserting the temp and humidity data into SQL
               
    for i in objects:
        dataInsert = "INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)" % (i[0], i[1], i[2])
        cursor.execute(dataInsert)
        cnxn.commit()
        
syncfromlocal()
print(objects)