import vehicle as gr
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation
from keras.optimizers import RMSprop
from keras.models import load_model
import random
import time,sys,pygame

numOst = 15
N=15
gamma = 0.9
point = 10
penalty = -100
model = Sequential()
model.add(Dense(5, init="lecun_uniform", input_shape=(5,)))
model.add(Activation('relu'))
model.add(Dense(160, init="lecun_uniform"))
model.add(Activation('relu'))
#model.add(Dense(160, init="lecun_uniform"))
#model.add(Activation('relu'))
model.add(Dense(3, init="lecun_uniform"))
model.add(Activation('linear'))

rms = RMSprop()
model.compile(loss='mse', optimizer=rms)



def initGame():
    g=gr.Vehicle((3,3)) # ho scelto questa posizione a caso
    obstacles=list()
    for i in range(numOst):
        poz=(random.randint(1,14),random.randint(1,14))
        if poz != (2,2):
            obstacles.append(poz)
    i=1
    while(i<=N-2):
        poz = (0, i)
        poz1 = (i, 0)
        poz2 = (N - 1, i)
        poz3 = (i, N - 1)
        obstacles.append(poz)
        obstacles.append(poz1)
        obstacles.append(poz2)
        obstacles.append(poz3)
        i+=1

    obstacles.append((0,0))
    obstacles.append((14,14))
    obstacles.append((0,14))
    obstacles.append((14,0))
    return g,obstacles

def testAlgo():
    g,obstacles= initGame()
    M = 600
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    pygame.init()
    size = (M, M)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Simulation")
    #clock = pygame.time.Clock()
    done=False
    while not done and g.dead==0:
        distances=calcolateDistances(g,obstacles)
        qval = model.predict(distances.reshape(1, 5), batch_size=1)
        action = np.argmax(qval)
        print(action)
        g.move_gir(action)
        checkCollision(g,obstacles)

        # la grafica
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
        screen.fill(BLACK)
        # riparti da capo ogni volta
        for o in obstacles:
            posizione = (40 * o[0], 40 * o[1], 40, 40)
            pygame.draw.rect(screen, RED, posizione) # obstacles

        position=((g.pos[0]*40)+20,(g.pos[1]*40)+20)
        pygame.draw.circle(screen,WHITE,position,10) # player
        pygame.display.flip()
        time.sleep(0.2)
    pygame.quit()



def train():
    epochs = 1000
    epsilon = 1
    total_deaths=0
    for i in range(epochs):
        g,obstacles = initGame()
        status=0
        j=0
        while status!=1 and j<20: # check if dead or all vehicles are dead

            distances = np.zeros(5)
            distances = calcolateDistances(g,obstacles)

            qval = model.predict(distances.reshape(1, 5), batch_size=1)
          
            if (random.random() < epsilon):
                action = np.random.randint(0,3)
            else:
                action = np.argmax(qval)

            g.move_gir(action)

            newDistances = calcolateDistances(g,obstacles)

            reward = getReward(g,obstacles)

            newQ = model.predict(newDistances.reshape(1, 5), batch_size=1)
            maxQ = np.max(newQ)

            y = np.zeros((1, 3))
            y[:] = qval[:]
            if reward == penalty:
                update = reward
                status=1
                total_deaths+=1
            else:
                update = reward + (gamma * maxQ)

            y[0][action] = update
            model.fit(distances.reshape(1, 5), y, batch_size=1, nb_epoch=1, verbose=0)
            j+=1

        if epsilon > 0.1:
            epsilon -= 1/epochs

        if(i%50==0):
            print(str((i/epochs)*100))
    print(total_deaths)
    model.save('my_model.h5')

def calcolateDistances(g,obstacles):
    distances = np.zeros(5)
    j=-2
    gir_prov=gr.Vehicle((0 , 0))
    while(j<=2):   
        action=g.old_action + j
        if action > 0:
            action = action % 8
        if action < 0:
            action = action + 8

        gir_prov.pos = g.pos
        for i in range(6):
            gir_prov.update_pos(action)
            if(checkCollision(gir_prov,obstacles)):
                distances[j+2] =  i + 1
                break
        if(i==5):
            distances[j+2]=6
        j+=1
    
    return distances

def getReward(g,obstacles):
    if checkCollision(g,obstacles):
        gain = penalty
    else:
        gain = point
    return gain

def checkCollision(g,obstacles):
    for o in obstacles:
        if o[0]==g.pos[0] and o[1]==g.pos[1]:
            g.dead=1
            return True
    return False

while(1):
    a=input("Train, test or kill: ")
    if(a == '1'):
        print("Inizio del training")
        train()
        print("Finito")
    elif a=='2':
        model = load_model('my_model.h5')
        testAlgo()
    elif a=='3':
        break
