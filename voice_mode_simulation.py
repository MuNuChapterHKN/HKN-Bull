import threading
import socket
import sys

# Duty cycle for right and left motor
right_dc = 0
left_dc = 0

def server():
    global right_dc
    global left_dc 
    global tL
    global tR
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    hostname = input("Insert hostname to start: ")
    while tL == None and tR == None:
        pass
    tL.start()
    tR.start()

    print(hostname + "Listening on port 2000")
    server_address = (hostname, 2000)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            # Receive the data
            while True:
                data = connection.recv(1024)
                if data:
                    dec = data.decode()
                    if dec == "1":
                        left_dc = 100
                        right_dc = 100
                    elif dec == '2':
                        left_dc = 0
                        right_dc = 100
                    elif dec == '0':
                        left_dc = 100
                        right_dc = 0
                    elif dec == '-1':
                        left_dc = 0
                        right_dc = 0
                    print("Sending data back to the client")
                    connection.sendall(data)
                else:
                    print('no more data from')
                    break

            
        finally:
            # Clean up the connection
            connection.close()

def left_motor():
    while True:
        print("Left: " + str(left_dc))

def right_motor():
    while True:
        print("Right: " + str(right_dc))      

if __name__ == '__main__':
    try:
        tS = threading.Thread(target=server, args = [])
        tS.daemon = True # se il processo chiamante finisce muore anche il thread
        tS.start()

        
        tL = threading.Thread(target = left_motor, args = [])
        tL.daemon = True
        # tL.start()

        tR = threading.Thread(target = right_motor, args = [])
        tR.daemon = True
        # tR.start()
    except:
        print ("Error: unable to start thread")

    while True:
        pass