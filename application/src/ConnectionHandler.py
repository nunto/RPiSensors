import socket


class ConnectionHandler:
    # Host to check
    REMOTE_HOSTNAME = 'www.google.com'

    def __init__(self):
        pass

    ## @brief Checks cocnnection to internet
    #  @return Returns a boolean, True if connected and False if disconnected        
    def is_connected(self):
        try:
            host = socket.gethostbyname(ConnectionHandler.REMOTE_HOSTNAME)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False
    
