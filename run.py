# Libraries
from keras.models import load_model
import RPi.GPIO as GPIO
import time
import threading
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO Pins
GPIO_TRIGGER = [18, 0, 0, 0, 0]
GPIO_ECHO = [24, 0, 0, 0, 0]

max_sight = 2
min_sight = 0.05
sleep_time = 0.03

# TO TEST IF WORKS
right_coefficient = 1
left_coefficient = 1

# set GPIO direction (IN / OUT)
for i in range(0, 5):
    GPIO.setup(GPIO_TRIGGER[i], GPIO.OUT)
    GPIO.setup(GPIO_ECHO[i], GPIO.IN)

def getdistances():
    distances = [0, 0, 0, 0, 0]
    for i in range(0, 5):
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
        distance = (TimeElapsed * 34300) / 2
        # adjust to coerent values
        if distance >= max_sight:
            distance = max_sight
        if distance < min_sight:
            return 0
        # brings data in range 1-6
        distances[i] = round(distance * 3)
        
    return distances

if __name__ == '__main__':
    model = load_model('my_model.h5')
    try:
        t1 = threading.Thread(target=right_motor_as, args = [])
        t1.daemon = True # se il processo chiamante finisce muore anche il thread
        t2 = threading.Thread(target=left_motor_as, args = [t])
        t2.daemon = True
        t1.start()
        t2.start()
    except:
        print ("Error: unable to start thread")

    # Main loop
    while True:
        distances =  getdistances()
        if distances == 0:
            print("Robot has hit an object")
            break
        move = model.predict(distances.reshape(1, distances), batch_size=1)
        new_action_right = 0
        new_action_left = 0
        if move == 0: # Dritto
            new_action_left = 1
            new_action_right = 1
            right_coefficient = 1
            left_coefficient = 1
        elif move == 2: # Destra
            new_action_left = 1
            new_action_right = 0.5
            right_coefficient -= 0.5
            left_coefficient = 1
        elif move == 1: # Sinistra
            new_action_left = 0.5
            new_action_right = 1
            left_coefficient -= 0.5
            right_coefficient = 1
        try:
            t1 = threading.Thread(target=right_motor, args = [new_action_right])
            t1.daemon = True # se il processo chiamante finisce muore anche il thread
            t2 = threading.Thread(target=left_motor, args = [new_action_left])
            t2.daemon = True
            t1.start()
            t2.start()
        except:
            print ("Error: unable to start thread")
        time.sleep(sleep_time)

# Funzioni per testare i threads
def right_motor(r):
    print("Destra: ", r)
def left_motor(l):
    print("Sinistra: ", l)

left_power = 100
right_power = 100
time_cycles = 10
sleep_coef = (sleep_time / 3) / time_cycles
def right_motor_as():   
    for i in range(0, time_cycles):
        left_power -= ((1 - left_coefficient) * sleep_coef) * left_power
        time.sleep(sleep_coef)
    time.sleep(sleep_coef * time_cycles)
    for i in range(0, time_cycles):
        left_power += ((1 - left_coefficient) * sleep_coef) * left_power
def left_motor_as():
    for i in range(0, time_cycles):
        right_power -= ((1 - left_coefficient) * sleep_coef) * right_power
    time.sleep(sleep_coef * time_cycles)
    for i in range(0, time_cycles):
        right_power += ((1 - left_coefficient) * sleep_coef) * right_power
        time.sleep(sleep_coef)

