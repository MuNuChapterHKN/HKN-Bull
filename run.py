# Libraries
from keras.models import load_model
import RPi.GPIO as GPIO
import time
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO Pins
GPIO_TRIGGER = [18, 0, 0, 0, 0]
GPIO_ECHO = [24, 0, 0, 0, 0]

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
        if distance >= 2:
            distance = 2
        if distance < 0.05:
            return 0
        distances[i] = round(distance * 3)
        
    return distances

if __name__ == '__main__':
    model = load_model('my_model.h5')
    # Main loop
    while True:
        distances =  getdistances()
        if distances == 0:
            print("Robot has hit an object")
            break
        move = model.predict(distances.reshape(1, distances), batch_size=1)

