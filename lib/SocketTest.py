import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    host_ip = socket.gethostbyname('www.google.com')
    print("yes")
except:
    print("no")