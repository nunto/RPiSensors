from threading import Thread, Semaphore
import threading
import time
import sys
import socket
def connectiontest():
    global x
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_connected.acquire()
    while(x <100):
        try:
            host_ip = socket.gethostbyname('www.google.com')
            print("yes")
        except:
            print("no")
        x = x +1
    is_connected.release()
x=0
y=0
is_connected = Semaphore(1)
#Define a function
def increment1():
    is_connected.acquire()
    global x
    is_connected.release()
    print("x = "+ str(x))
    x = x+1

def increment2():
    global y
    is_connected.acquire()
    while(y <100):    
        print("y = "+str(y))
        y = y+1
        #sys.exit()
    is_connected.release()

class myThread1 (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print("Starting: " + self.name)
        connectiontest()

class myThread2 (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print("Starting: " + self.name)
        increment2()


thread1 = myThread1('xthread')
thread2 = myThread2('ythread')

thread1.start()
thread2.start()
thread1.join()
thread2.join()

"""
try:
    _thread.start_new_thread(increment1, ())
    _thread.start_new_thread(increment2, ())
except:
    print ("unable to start thread")
"""