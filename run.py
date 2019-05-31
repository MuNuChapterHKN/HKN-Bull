# Libraries
from keras.models import load_model
import RPi.GPIO as GPIO
import time
import threading
from gpiozero import PWMOutputDevice
import numpy as np
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
GPIO_TRIGGER = [13, 19, 7]
GPIO_ECHO = [15, 21, 11]

max_sight = 2
min_sight = 0.05
sleep_time = 1

# TO TEST IF WORKS
right_coefficient = 1
left_coefficient = 1


PWM_FORWARD_LEFT_PIN = "BOARD37"  # IN1 - Forward Drive
PWM_REVERSE_LEFT_PIN = "BOARD35"   # IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_FORWARD_RIGHT_PIN = "BOARD33"  # IN1 - Forward Drive
PWM_REVERSE_RIGHT_PIN = "BOARD31"   # IN2 - Reverse Drive

# Initialise objects for H-Bridge PWM pins
# Set initial duty cycle to 0 and frequency to 1000
forwardLeft = PWMOutputDevice(PWM_FORWARD_LEFT_PIN, True, 0, 1000)
reverseLeft = PWMOutputDevice(PWM_REVERSE_LEFT_PIN, True, 0, 1000)

forwardRight = PWMOutputDevice(PWM_FORWARD_RIGHT_PIN, True, 0, 1000)
reverseRight = PWMOutputDevice(PWM_REVERSE_RIGHT_PIN, True, 0, 1000)


# set GPIO direction (IN / OUT)
for i in range(0, 3):
    GPIO.setup(GPIO_TRIGGER[i], GPIO.OUT)
    GPIO.setup(GPIO_ECHO[i], GPIO.IN)

def getdistances():
    distances = np.zeros(3)
    for i in range(0, 3):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER[i], True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER[i], False)
    
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(GPIO_ECHO[i]) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(GPIO_ECHO[i]) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 200
        # adjust to coerent values
        if distance >= max_sight:
            distance = max_sight
        if distance < min_sight:
            return 0
        # brings data in range 1-6
        distances[i] = int(round(distance)*3)
        
    return distances

if __name__ == '__main__':
    model = load_model('my_model.h5')
    '''
    try:
        t1 = threading.Thread(target=right_motor_as, args = [])
        t1.daemon = True # se il processo chiamante finisce muore anche il thread
        t2 = threading.Thread(target=left_motor_as, args = [])
        t2.daemon = True
        t1.start()
        t2.start()
    except:
        print ("Error: unable to start thread")
    '''
    # Main loop
    while True:
        distances =  getdistances()
        print(distances)
        if np.all(distances==0):
            print("Robot has hit an object")
            #break
        qval = model.predict(distances.reshape(1, 3), batch_size=1)        
        move = np.argmax(qval)
        new_action_right = 0
        new_action_left = 0
        if move == 0: # Dritto
            print("Dritto")
            forwardDrive()
            sleep(2)
            allStop()
        elif move == 2: # Destra
            print("Destra")
            forwardTurnRight()
            sleep(2)
            allStop()
        elif move == 1: # Sinistra
            print("Sinistra")
            forwardTurnLeft()       
            sleep(2)
            allStop()
        
        time.sleep(sleep_time)

# Funzioni per testare i threads
def right_motor(r):
    print("Destra: ", r)
def left_motor(l):
    print("Sinistra: ", l)

def allStop():
    forwardLeft.value = 0
    reverseLeft.value = 0
    forwardRight.value = 0
    reverseRight.value = 0
 
def forwardDrive():
    forwardLeft.value = 1.0
    reverseLeft.value = 0
    forwardRight.value = 1.0
    reverseRight.value = 0
 
def reverseDrive():
    forwardLeft.value = 0
    reverseLeft.value = 1.0
    forwardRight.value = 0
    reverseRight.value = 1.0
 
def spinLeft():
    forwardLeft.value = 0
    reverseLeft.value = 1.0
    forwardRight.value = 1.0
    reverseRight.value = 0
 
def SpinRight():
    forwardLeft.value = 1.0
    reverseLeft.value = 0
    forwardRight.value = 0
    reverseRight.value = 1.0
 
def forwardTurnLeft():
    forwardLeft.value = 0.2
    reverseLeft.value = 0
    forwardRight.value = 0.8
    reverseRight.value = 0
 
def forwardTurnRight():
    forwardLeft.value = 0.8
    reverseLeft.value = 0
    forwardRight.value = 0.2
    reverseRight.value = 0
 
def reverseTurnLeft():
    forwardLeft.value = 0
    reverseLeft.value = 0.2
    forwardRight.value = 0
    reverseRight.value = 0.8
 
def reverseTurnRight():
    forwardLeft.value = 0
    reverseLeft.value = 0.8
    forwardRight.value = 0
    reverseRight.value = 0.2

