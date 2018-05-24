import vehicle as gr
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation
from keras.optimizers import RMSprop
from keras.models import load_model
import random
import time,sys,pygame

M =720
#storicoPos = []
#nPos = 5
startX = 3
startY = 3
numOst = 60
N = M / 40  # dimensione matrice
gamma = 0.9
point = 10
penalty = -100
model = Sequential()
model.add(Dense(3, init="lecun_uniform", input_shape=(3,)))
model.add(Activation('relu'))
model.add(Dense(160, init="lecun_uniform"))
model.add(Activation('relu'))
model.add(Dense(160, init="lecun_uniform"))
model.add(Activation('relu'))
model.add(Dense(3, init="lecun_uniform"))
model.add(Activation('linear'))

rms = RMSprop()
model.compile(loss='mse', optimizer=rms)



def initGame():
    #inizializzo il veicolo
    g = gr.Vehicle((startX, startY))  # ho scelto questa posizione a caso
    obstacles = list()  # creo gli ostacoli in posizione random
    for i in range(numOst):
        poz = (random.randint(1, N - 1), random.randint(1, N - 1))
        if poz != (startX, startY):
            obstacles.append(poz)
    i = 1
    #inserisco i bordi
    while(i <= N - 2):
        poz = (0, i)
        poz1 = (i, 0)
        poz2 = (N - 1, i)
        poz3 = (i, N - 1)
        #poz3 = (i, 6)
        obstacles.append(poz)
        obstacles.append(poz1)
        obstacles.append(poz2)
        obstacles.append(poz3)
        i += 1

    #inserisco gli angoli
    obstacles.append((0, 0))
    obstacles.append((N - 1, N - 1))
    obstacles.append((0, N - 1))
    obstacles.append((N - 1, 0))
    return g, obstacles


def testAlgo():
    g, obstacles = initGame()
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    pygame.init()
    size = (M, M)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Simulation")
    #clock = pygame.time.Clock()
    done = False
    while not done and g.dead == 0:
        distances = calcolateDistances(g, obstacles)
        qval = model.predict(distances.reshape(1, 3), batch_size=1)
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

        kMax = int(M / 40)
        for i in range(kMax):
            pygame.draw.line(screen, GRAY, (0, i*40), (M, i*40), 1)
            pygame.draw.line(screen, GRAY, (i * 40, 0), (i * 40, M), 1)

        position = ((g.pos[0]*40)+20, (g.pos[1] * 40) + 20)
        pygame.draw.circle(screen, WHITE, position, 10)  # player
        pygame.display.flip()
        time.sleep(0.5)
    pygame.quit()



def train():
    epochs = 1000
    epsilon = 1
    total_deaths = 0
    for i in range(epochs):
        g, obstacles = initGame()
        status = 0
        j = 0
        while status != 1 and j < 20:  # check if dead or all vehicles are dead

            distances = np.zeros(3)
            distances = calcolateDistances(g, obstacles)

            qval = model.predict(distances.reshape(1, 3), batch_size=1)  # valori senza la prossima mossa
          
            if random.random() < epsilon:  # uso un valore casuale come mossa se tale valore è minore di epsilon
                action = np.random.randint(0, 3)
            else:
                action = np.argmax(qval)

            g.move_gir(action)

            newDistances = calcolateDistances(g, obstacles)  # calcolo le nuove distanze in base alla mossa fatta

            reward = getReward(g, obstacles, action)  # controllo se ha colpito un ostacolo

            newQ = model.predict(newDistances.reshape(1, 3), batch_size=1)  # valori con la prossima mossa

            maxQ = np.max(newQ)

            y = np.zeros((1, 3))
            y[:] = qval[:]
            if reward == penalty:
                update = reward
                status = 1
                total_deaths += 1
            else:
                update = reward + (gamma * maxQ)

            y[0][action] = update

            model.fit(distances.reshape(1, 3), y, batch_size=1, nb_epoch=1, verbose=0)

            j += 1

        if epsilon > 0.1:
            epsilon -= 1/(epochs)

        if(i % 50) == 0:
            #print(str((i/epochs) * 100))
            print("{0:.2f}".format((i/epochs) * 100))
    print("Total deaths: " + str(total_deaths) + "\nPercentuale : " + "{0:.2f}".format((total_deaths / epochs * 100)) + "%")
    model.save('my_model.h5')

def calcolateDistances(g, obstacles):
    distances = np.zeros(3)
    j = -1
    gir_prov = gr.Vehicle((0, 0))
    while j <= 1:
        action = g.old_action + j
        if action > 0:
            action = action % 8
        if action < 0:
            action = action + 8

        gir_prov.pos = g.pos

        for i in range(6):
            gir_prov.update_pos(action)
            if checkCollision(gir_prov, obstacles):
                distances[j+1] = i + 1
                break
        if i == 5:
            distances[j + 1] = 6
        j += 1
    
    return distances

# def controllaContenuto(arrayPiccolo, dim):
#     ripetizioni = 0
#     for i in range (len(storicoPos) - 2 * dim + 1):
#         if arrayPiccolo == storicoPos[i:i + dim - 1]:
#             ripetizioni += 1
#     return ripetizioni


# def controllaRidondanza():
#     i = 3
#     ripetizioni = 0
#     last = len(storicoPos) - 1
#     while i < nPos:
#         sottoVettore = storicoPos[(last - i): last]
#         ripetizioni = controllaContenuto(sottoVettore,i)
#         if ripetizioni > 2:
#             return True
#     return False

def getReward(g, obstacles, action):
    #pos = g.pos
    #storicoPos.append(pos)

    # if len(storicoPos) > 10:
    #     storicoPos.remove(storicoPos[0])
    # if len(storicoPos) > nPos and (controllaRidondanza()):
    #     gain = -5
    # elif
    gain = 0
    if checkCollision(g, obstacles):
        gain = penalty
    else:
        if (action == 0):
            gain += 2

        gain += point
    return gain

def checkCollision(g, obstacles):
    for o in obstacles:
        if o[0] == g.pos[0] and o[1] == g.pos[1]:
            g.dead = 1
            return True
    return False


while 1:
    a = input("Train (1), test (2) or kill (3): ")
    if a == '1':
        print("Inizio del training")
        train()
        print("Finito")
    elif a == '2':
        model = load_model('my_model.h5')
        testAlgo()
    elif a == '3':
        break
