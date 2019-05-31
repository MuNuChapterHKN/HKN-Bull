from gpiozero import PWMOutputDevice
from time import sleep
 
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
def init():
	

 
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

def destra():
	init()
	forwardTurnRight()
	allStop()

def sinistra(): 
	init()
	forwardTurnLeft()
	allStop()

def dritto():
	init()
	forwardDrive()
	allStop()

