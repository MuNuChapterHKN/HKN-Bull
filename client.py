#!/usr/bin/python3

"""Converts voice into robot instruction."""
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import sys
from socket import *

aiy.i18n.set_language('it-IT')
myHost = input("Please insert server host: ")
myPort = 2000

def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    while aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press button to send commands to the robot')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
                s.connect((serverHost, serverPort)) # connect to server on the port
                if text == 'robot dritto':
                    s.send('1')
                    data = s.recv(1024)
                elif text == 'robot destra':
                    s.send('2')
                    data = s.recv(1024)
                elif text == 'robot sinistra':
                    s.send('3')
                    data = s.recv(1024)
                elif text == 'robot fermo':
                    s.send('-1')
                    data = s.recv(1024)
                print(data)
            else:
                print("Cannot recognize speech")
