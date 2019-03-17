import numpy as np
import threading

class Vehicle:
    pos = (0, 0)
    pos_old = (0, 0)
    dir = (0, 0)
    dead = 0
    old_action = 3
    actions = list()

    def __init__(self, pos_iniz):
        self.pos = pos_iniz
        self.actions.append((-1,0))
        self.actions.append((-1,1))
        self.actions.append((0,1))
        self.actions.append((1,1))
        self.actions.append((1,0))
        self.actions.append((1,-1))
        self.actions.append((0,-1))
        self.actions.append((-1,-1))

    def update_pos(self, action):
         tup = ((self.pos[0]+(self.actions[action])[0]),(self.pos[1]+(self.actions[action])[1]))  # il panico
         self.pos = tup

         self.old_action = action

    def move_gir(self,move):
        # changing position
        new_action = 0
       
        if move == 0:
            new_action = self.old_action  # Dritto
        elif move == 1:
            new_action = (self.old_action+1)%8  # Sinistra
        elif move == 2:
            if self.old_action == 0:
                new_action = 7  # Destra
            else:
                new_action = self.old_action-1
        self.update_pos(new_action)

    def move_vehicle(self,move):
        new_action_right = 0
        new_action_left = 0
        if move == 0: # Dritto
            new_action_left = 1
            new_action_right = 1
        elif move == 2: #Destra
            new_action_left = 1
            new_action_right = 0.5
        elif move == 1: #Sinistra
            new_action_left = 0.5
            new_action_right = 1
        # Thread per gestire contemporaneamente motore destro e sinistro
        try:
            t1 = threading.Thread(target=right_motor, args = [new_action_right])
            t1.daemon = True # se il processo chiamante finisce muore anche il thread
            t2 = threading.Thread(target=left_motor, args = [new_action_left])
            t2.daemon = True
            t1.start()
            t2.start()
        except:
            print ("Error: unable to start thread")

# Funzioni per testare i threads
def right_motor(r):
    print("Destra: ", r)
def left_motor(l):
    print("Sinistra: ", l)



