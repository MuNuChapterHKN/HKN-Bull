import RPi.GPIO as GPIO
import time

def measure(TRIG, ECHO):
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


GPIO.setmode(GPIO.BOARD)

TRIG1 = 7
TRIG2 = 8
TRIG3 = 9
ECHO1 = 11
ECHO2 = 12
ECHO3 = 13

print("Distance measurement in progress")

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(TRIG3, GPIO.OUT)

GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.output(TRIG1, GPIO.LOW)
GPIO.output(TRIG2, GPIO.LOW)
GPIO.output(TRIG3, GPIO.LOW)

print("Waiting for sensor to settle")
time.sleep(2)

while(True):
    distance1 = measure(TRIG1, ECHO1)
    distance2 = measure(TRIG2, ECHO2)
    distance3 = measure(TRIG3, ECHO3)
    print("[Distance] 1--> " +  str(distance1) + "cm\t2--> " + str(distance2) + "cm\t3--> "+ str(distance3) + "cm") 
    sleep(1)

GPIO.cleanup()

