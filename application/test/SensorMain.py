import time
from threading import Thread
from SensorDataRetrieval import SensorDataRetrieval
from DataStorage import DataStorage
from ConnectionHandler import ConnectionHandler
from datetime import datetime

def current_time() -> int:
    return int(time.mktime(datetime.now().timetuple()))

def dht_process(sdr, ds, status: bool):
    print('in dht_process')
    dht_data = sdr.dht_reading()
    timestamp = current_time()
    temp = int(dht_data[0])
    hum = int(dht_data[1])

    if (status):
        ds.SQL_insert(timestamp, temp, hum)
    else:
        ds.offline_save(timestamp, temp, hum)

if (__name__ == '__main__'):
    dht_interval = 5 # Get this from GUI later
    # Other intervals here---
    #---
    intervals = [dht_interval]
    is_local_data = False
    dht_last_update = 0
    thermal_last_update = 0

    # Instantiating relevant sensor objects
    sdr = SensorDataRetrieval()
    ds = DataStorage()
    ch = ConnectionHandler()


    # TODO: Add a check for each sensor time, only insert if it is time for them
    while (True):
        if (ch.is_connected()):
            print('connected')
            if (is_local_data):
                ds.data_sync()
                is_local_data = False

            if (dht_last_update + dht_interval <= current_time()):
                dht_last_update = current_time()
                dht_thread = Thread(target = dht_process, args=(sdr, ds, True))
                dht_thread.start()
        else:
            print('not connected')
            # Save locally
            if (dht_last_update + dht_interval <= current_time()):
                dht_last_update = current_time()
                dht_thread = Thread(target = dht_process, args=(sdr, ds, False))
                dht_thread.start()
            if (not is_local_data):
                is_local_data = True

        dht_thread.join()
        time.sleep(min(intervals))