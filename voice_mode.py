import RPi.GPIO as GPIO 
import threading
import socket     
import sys

# Duty cycle for right and left motor
right_dc = 0
left_dc = 0

GPIO.setmode(GPIO.BOARD)  # Set Raspberry to use pin number when referencing GPIO pin

# Left motor
GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwmLeft = GPIO.PWM(12, 100)   # Initialize PWM on pwmPin 100Hz frequency

# Right motor
GPIO.setup(13, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwmRight = GPIO.PWM(13, 100)   # Initialize PWM on pwmPin 100Hz frequency

# Thread who acts as a server and listen for TCP connections
def server():
    # These variables need to be declared as global
    global right_dc
    global left_dc 
    global tL
    global tR

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Insert IP for this machine and acts as a starter point
    hostname = input("Insert hostname of this server to start: ")
    print(hostname + " listening on port 2000")
    # Wait until the threads for the motors are not created
    while tL == None and tR == None:
        pass
    # Start motors' thread from here
    tL.start()
    tR.start()

    # Binding socket
    server_address = (hostname, 2000)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)

    # Main server loop
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            # Receive the data
            while True:
                # Receive up tp 1 kB of data
                data = connection.recv(1024)
                if data:
                    # If there is data decode it
                    dec = data.decode()
                    
                    # Choose what to do based on client's instructions
                    if dec == "1":
                        # Go straight ahead
                        left_dc = 100
                        right_dc = 100
                    elif dec == '2':
                        # Turn left
                        left_dc = 0
                        right_dc = 100
                    elif dec == '0':
                        # Turn right
                        left_dc = 100
                        right_dc = 0
                    elif dec == '-1':
                        # Stop
                        left_dc = 0
                        right_dc = 0
                    # Sends the data back
                    print("Sending data back to the client")
                    connection.sendall(data)
                else:
                    print('no more data from')
                    break
        finally:
            # Clean up the connection
            connection.close()

# Thread for left motor
def left_motor():
    pwmLeft.start(left_dc)
    old_dc = left_dc
    try:
        while True:
            if old_dc != left_dc:
                pwmLeft.ChanceDutyCycle(left_dc)
                print("Left: " + str(left_dc))
                old_dc = left_dc
    except KeyboardInterrupt:
        print("Ctl C pressed - stopping left motor")

    # stop PWM
    pwmLeft.stop()                         

# Thread for right motor
def right_motor():
    pwmRight.start(right_dc)
    old_dc = right_dc
    try:
        while True:
            if old_dc != right_dc:
                pwmRight.ChangeDutyCycle(right_dc)
                print("Right: " + str(right_dc))  
                old_dc = right_dc   
    except KeyboardInterrupt:
        print("Ctl-C pressed - stopping right motor")

    # stop PWM
    pwmRight.stop()                         

# Create threads
if __name__ == '__main__':
    try:
        tS = threading.Thread(target=server, args = [])
        tS.daemon = True # If the caller dies so the thread
        tS.start()

        
        tL = threading.Thread(target = left_motor, args = [])
        tL.daemon = True

        tR = threading.Thread(target = right_motor, args = [])
        tR.daemon = True
    except:
        print ("Error: unable to start thread")

    # Infinite main loop
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctl-C pressed - ending program")

    # resets GPIO ports used back to input mode
    GPIO.cleanup()                     