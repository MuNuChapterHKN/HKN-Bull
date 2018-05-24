import numpy as np

class Vehicle:
    pos = (0,0)
    pos_old=(0,0)
    dir=(0,0)
    dead=0
    old_action=3
    actions=list()

    def __init__(self,pos_iniz):
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
         tup=((self.pos[0]+(self.actions[action])[0]),(self.pos[1]+(self.actions[action])[1])) # il panico
         self.pos=tup

         self.old_action=action

    def move_gir(self,move):
        #changing position
        new_action=0
       
        if move==0:
            new_action=self.old_action #Dritto
        elif move==1:
            new_action=(self.old_action+1)%8 #Destra
        elif move==2:
            if self.old_action==0:
                new_action=7 #Sinistra
            else:
                new_action=self.old_action-1
        self.update_pos(new_action)







