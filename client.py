#!/usr/bin/python3

"""Converts voice into robot instruction."""
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import sys
from socket import *

aiy.i18n.set_language_code('it-IT')
myHost = input("Please insert server host: ")
myPort = 2000

def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    data = " "
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press button to send commands to the robot')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
                s.connect((myHost, myPort)) # connect to server on the port
                if text == 'robot dritto':
                    s.send('1'.encode())
                    data = s.recv(1024).decode()
                elif text == 'robot destra':
                    s.send('2'.encode())
                    data = s.recv(1024).decode()
                elif text == 'robot sinistra':
                    s.send('3'.encode())
                    data = s.recv(1024).decode()
                elif text == 'robot stop':
                    s.send('-1'.encode())
                    data = s.recv(1024).decode()
                print(data)
            else:
                print("Cannot recognize speech")

if __name__ == '__main__':
	main()
