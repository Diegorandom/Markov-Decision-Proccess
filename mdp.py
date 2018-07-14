"""
Diego Ignacio Ortega A01227020 

Referencias de guía:
https://gist.github.com/annisap/523c2914fc7ecedc35380cd1988da3d6

"""


import numpy as np
import random
import pprint
import sys
import matplotlib.pylab as plt
from cuadricula import Cuadricula

width, height = 100, 100;
Matrix = [[0 for x in range(width)] for y in range(height)]
on = 1
contAutosWe = 0
contAutosNs = 0
newAutos = []
newAutos2 = []
iteracioneSemaf = 0
sentido = 'NS'
traficoNs = 'Por determinar'
traficoWe = "Por determinar"

"""The pprint module provides a capability to “pretty-print” arbitrary Python data structures in a form which can be used as input to the interpreter."""
pp = pprint.PrettyPrinter(indent=2)

cuad = Cuadricula()

"""El Value Iteration algorithm is un procedimiento iterativo que calcula la utilidad esperada de cada estado de una cuadricula utilizando las utilidades de los estados vecinos hasta que las utilidades calculadas entre 2 iteraciones están lo suficientemente cerca

Entre más pequeño sea theta mas precision tendrá el algoritmo
Esto quiere decir que si delta < theta entonces significa que la diferencia entre la utilidad previa del estado y la utilidad actual del estado es lo suficientemente pequeña para considerar que el algoritmo ha convergido

"""

def valueIteration(cuad, theta=0.0001, factorDescuento=1.0):
    #Hacia adelante toma el estado y el valor de este y utiliza la ecuacion de Bellman para determinar cuales son los posibles movimientos y cual de ellos tiene la utilidad mas alta
    def haciaAdelante(state, V):
        A = np.zeros(cuad.numAcciones)
        for a in range(cuad.numAcciones):
            #Por cada iteracion se calcula el valor de la utilidad de cada posible estado para despues determinar cual es el mejor movimiento posible
            for prob, next_state, reward, done in cuad.transiciones[state][a]:
                A[a] += prob * (reward + factorDescuento * V[next_state])
        return A
    
    V = np.zeros(cuad.numStates)
    while True:
        delta = 0
        for s in range(cuad.numStates):
            A = haciaAdelante(s, V)
            valorMejorAccion = np.max(A)
            delta = max(delta, np.abs(valorMejorAccion - V[s]))
            V[s] = valorMejorAccion        
        if delta < theta:
            break
    
    poliza = np.zeros([cuad.numStates, cuad.numAcciones])
    for s in range(cuad.numStates):
        #El arreglo A calcula la mejor accion posible dado el estado y el valor actual del estado
        A = haciaAdelante(s, V)
        mejorAccion = np.argmax(A)
        #El mejor movimiento posible es utilizado para colocar en la posicion de estado y se le da valr = 1.0 a la poliza
        poliza[s, mejorAccion] = 1.0
    
    return poliza, V

poliza, v = valueIteration(cuad)


print(" poliza (0=N, 1=E, 2=S, 3=W, 4 = NE , 5 =SE, 6 = SW, 7 = NW):")


policyMatrix = np.reshape(np.argmax(poliza, axis=1), cuad.dimensiones)


print(policyMatrix)  #Policy Solucion 


print("")
print(" Value Function:")
valueFunctionMatrix = v.reshape(cuad.dimensiones)
print(valueFunctionMatrix)
print("")

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
plt.imshow(valueFunctionMatrix, interpolation='nearest', cmap=plt.cm.ocean)
plt.colorbar()
plt.show()

g = np.flipud(policyMatrix)
u = v = np.ones((100,100))
u = np.random.rand(100,100)
v = np.random.rand(100,100)

for n in range(5):
    for k in range(5):
        if g[n][k] == 0:
            u[n][k] = 0
            v[n][k] = 1
        elif g[n][k] == 4:
            u[n][k] = 1
            v[n][k] = 1
        elif g[n][k] == 1:
            u[n][k] = 1
            v[n][k] = 0
        elif g[n][k] == 5:
            u[n][k] = 1
            v[n][k] = -1
        elif g[n][k] == 2:
            u[n][k] = 0
            v[n][k] = -1
        elif g[n][k] == 6:
            u[n][k] = -1
            v[n][k] = -1
        elif g[n][k] == 3:
            u[n][k] = -1
            v[n][k] = 0
        else:
            u[n][k] = -1
            v[n][k] = 1

"""
autoGen() y autoGenNor() son funciones que generan el tráfico de forma aleatoria.
Es posible incrementar el tráfico cambiando el arreglo options entre las cuales la clase random elige que proporción de tráfico integrar en el cruce
"""
def autoGen():
    global contAutosWe
    global newAutos
    options = [3,1]
    newAutos = []
    for n in range(20):
        newAutos.append(random.choice(options))
    contAutosWe += newAutos.count(3)
    return 

def autoGenNor():
    global contAutosNs
    global newAutos2
    options = [2,1]
    newAutos2 = []
    for n in range(20):
        newAutos2.append(random.choice(options))
    contAutosNs += newAutos2.count(2)
    return

"""
revisionMov(fila,columc) se encarga de tomar una decisión alternativa a la poliza dado que esta se encuentre bloqueada por otro agente. Esta alternativa utiliza el arreglo valueFunctionMatrix y elige la alternativa cuya recompensa sea mayor 
"""
def revisionMov(j,i):
    global Matrix
    global valueFunctionMatrix
    
    if((j-1 == -1) and not (i-1 == -1)):   
        movimientos = [[j-1,i-1,-4000],[j-1,i,-4000],[j-1,i+1,-4000],[j,i-1,valueFunctionMatrix[j][i-1]],[j,i+1,valueFunctionMatrix[j][i+1]],[j+1,i-1,valueFunctionMatrix[j+1][i-1]],[j+1,i,valueFunctionMatrix[j+1][i]],[j+1,i+1,valueFunctionMatrix[j+1][i+1]],[j,i,valueFunctionMatrix[j][i]]]
    elif((i-1 == -1) and not (j-1 == -1)):
        movimientos = [[j-1,i-1,-4000],[j-1,i,valueFunctionMatrix[j-1][i]],[j-1,i+1,valueFunctionMatrix[j-1][i+1]],[j,i-1,-4000],[j,i+1,valueFunctionMatrix[j][i+1]],[j+1,i-1,-4000],[j+1,i,valueFunctionMatrix[j+1][i]],[j+1,i+1,valueFunctionMatrix[j+1][i+1]],[j,i,valueFunctionMatrix[j][i]]]
    elif((i-1 == -1) and (j-1 == -1)):
        movimientos = [[j-1,i-1,-4000],[j-1,i,-4000],[j-1,i+1,-4000],[j,i-1,-4000],[j,i+1,valueFunctionMatrix[j][i+1]],[j+1,i-1,-4000],[j+1,i,valueFunctionMatrix[j+1][i]],[j+1,i+1,valueFunctionMatrix[j+1][i+1]],[j,i,valueFunctionMatrix[j][i]]]
    else:
        movimientos = [[j-1,i-1,valueFunctionMatrix[j-1][i-1]],[j-1,i,valueFunctionMatrix[j-1][i]],[j-1,i+1,valueFunctionMatrix[j-1][i+1]],[j,i-1,valueFunctionMatrix[j][i-1]],[j,i+1,valueFunctionMatrix[j][i+1]],[j+1,i-1,valueFunctionMatrix[j+1][i-1]],[j+1,i,valueFunctionMatrix[j+1][i]],[j+1,i+1,valueFunctionMatrix[j+1][i+1]],[j,i,valueFunctionMatrix[j][i]]]
    
    openList = []
    
    for x in range(len(movimientos)):
        if ((Matrix[movimientos[x][0]][movimientos[x][1]] == 1) and(movimientos[x][1] != -1)):
                recompensa = movimientos[x][2]
                openList.append([recompensa,x])
    return openList

"""
Construcción de obstáculos que la poliza tomó en cuenta
"""
        
for y in range (len(Matrix)):
    for z in range (len(Matrix)):
        if 39<z<60 and 0<=y<100:
            Matrix[z][y] = 1
        if 39<y<60 and 0<=z<100:
            Matrix[z][y] = 1
        if 48<=z<=51 and 48<=y<=51:
            Matrix[z][y] = 0
        if (46<=z<=47 or 52<=z<=53) and (48<=y<=51):
            Matrix[z][y] = 0
        if (46<=y<=47 or 52<=y<=53) and (48<=z<=51):
            Matrix[z][y] = 0
        if(95<=z<=100) and (y==44):
            Matrix[z][y] = 0
        if(95<=z<=100) and (y==49):
            Matrix[z][y] = 0
        if(95<=z<=100) and (y==54):
            Matrix[z][y] = 0
        if(95<=y<=100) and (z==44):
            Matrix[z][y] = 0
        if(95<=y<=100) and (z==49):
            Matrix[z][y] = 0
        if(95<=y<=100) and (z==54):
            Matrix[z][y] = 0
        
"""
esteOeste(columna) se encarga de mover a los agentes de esta direccion hasta la meta objetivo

"""  
def esteOeste(columna):
    global Matrix
    global contAutosWe
    global contAutosNs
    global newAutos
    """Revision de cantidad de agentes y su eliminacion al llegar a la meta"""
    if columna == 0:
        for fila in range (len(Matrix)):
            if 39<fila<60:
                if Matrix[fila][0] == 3:
                    contAutosWe -= 1
                    Matrix[fila][0] = 1
        autoGen()
        for fila in range (len(Matrix)):
            if 39<fila<60:
                Matrix[fila][0] = newAutos[fila-40]
    if columna == 39:
        for fila in range (len(Matrix)):
            if 39<fila<60:
                if Matrix[fila][99] == 3:
                    contAutosWe -= 1
                    Matrix[fila][99] = 1
                if Matrix[fila][99] == 2:
                    contAutosNs -= 1
                    Matrix[fila][99] = 1
        
    for j in range (len(Matrix)):
        if (0<j<99 and 0<=columna<99):
            if Matrix[j][columna] == 3:
                
                """aplicacion de la poliza para agentes de norte-sur"""
                if(policyMatrix[j][columna] == 0 ) and (Matrix[j-1][columna] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j-1][columna] = 3
                elif(policyMatrix[j][columna] == 1) and (Matrix[j][columna+1] == 1):
                    Matrix[j][columna+1] = 3
                    Matrix[j][columna] = 1
                elif(policyMatrix[j][columna] == 2) and (Matrix[j+1][columna] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j+1][columna] = 3
                elif(policyMatrix[j][columna] == 3) and ( Matrix[j][columna-1] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j][columna-1] = 3
                elif(policyMatrix[j][columna] == 4) and (Matrix[j-1][columna+1] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j-1][columna+1] = 3
                elif(policyMatrix[j][columna] == 5) and (Matrix[j+1][columna+1] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j+1][columna+1] = 3
                elif(policyMatrix[j][columna] == 6) and (Matrix[j+1][columna-1] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j+1][columna-1] = 3
                elif(policyMatrix[j][columna] == 7) and ( Matrix[j-1][columna-1] == 1):
                    Matrix[j][columna] = 1
                    Matrix[j-1][columna-1] = 3
                else:
                    """En caso de que la poliza esté bloqueada se utiliza se genera una alternativa"""
                    poliza = revisionMov(j,columna)
                    if len(poliza) != 0:
                        sigMov = max(poliza)
                        if (sigMov[1] == 0):
                            Matrix[j][columna] = 1
                            Matrix[j-1][columna-1] = 3
                        elif sigMov[1] == 1:
                            Matrix[j][columna] = 1
                            Matrix[j-1][columna] = 3
                        elif sigMov[1] == 2:
                            Matrix[j][columna] = 1
                            Matrix[j-1][columna+1] = 3
                        elif sigMov[1] == 3:
                            Matrix[j][columna] = 1
                            Matrix[j][columna-1] = 3
                        elif sigMov[1] == 4:
                            Matrix[j][columna+1] = 3
                            Matrix[j][columna] = 1
                        elif sigMov[1] == 5:
                            Matrix[j][columna] = 1
                            Matrix[j+1][columna-1] = 3
                        elif sigMov[1] == 6:
                            Matrix[j][columna] = 1
                            Matrix[j+1][columna] = 3
                        elif sigMov[1] == 7:
                            Matrix[j][columna] = 1
                            Matrix[j+1][columna+1] = 3
                        elif sigMov[1] == 8:
                            Matrix[j][columna] = 3        

"""
norteSur(fila) se encarga de mover a los agentes de esta direccion hasta la meta objetivo

""" 
def norteSur(fila):
    global Matrix
    global contAutosNs
    global contAutosWe
    global newAutos2
    
    """Revision de cantidad de agentes y su eliminacion al llegar a la meta"""
    if fila == 0:
        for columna in range (len(Matrix)):
            if 39<columna<60:
                if (Matrix[0][columna] == 2):
                    contAutosNs -= 1
                    Matrix[0][columna] = 1
                
                
        autoGenNor()
        for columna in range (len(Matrix)):
            if 39<columna<60:
                Matrix[0][columna] = newAutos2[columna-40]
                
    if fila == 39:
        for columna in range (len(Matrix)):
            if 39<columna<60:
                if Matrix[99][columna] == 2:
                    contAutosNs -= 1
                    Matrix[99][columna] = 1
                if Matrix[99][columna] == 3:
                    contAutosWe -= 1
                    Matrix[99][columna] = 1
        
    for columna in range (len(Matrix)):
        if (0<columna<99 and 0<=fila<99):
            if Matrix[fila][columna] == 2:
                
                """aplicacion de la poliza para agentes de norte-sur"""
                if(policyMatrix[fila][columna] == 0 ) and (Matrix[fila-1][columna] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila-1][columna] = 2
                elif(policyMatrix[fila][columna] == 1) and (Matrix[fila][columna+1] == 1):
                    Matrix[fila][columna+1] = 2
                    Matrix[fila][columna] = 1
                elif(policyMatrix[fila][columna] == 2) and (Matrix[fila+1][columna] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila+1][columna] = 2
                elif(policyMatrix[fila][columna] == 3) and ( Matrix[fila][columna-1] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila][columna-1] = 2
                elif(policyMatrix[fila][columna] == 4) and (Matrix[fila-1][columna+1] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila-1][columna+1] = 2
                elif(policyMatrix[fila][columna] == 5) and (Matrix[fila+1][columna+1] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila+1][columna+1] = 2
                elif(policyMatrix[fila][columna] == 6) and (Matrix[fila+1][columna-1] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila+1][columna-1] = 2
                elif(policyMatrix[fila][columna] == 7) and ( Matrix[fila-1][columna-1] == 1):
                    Matrix[fila][columna] = 1
                    Matrix[fila-1][columna-1] = 2
                else:
                    """En caso de que la poliza esté bloqueada se utiliza se genera una alternativa"""
                    poliza = revisionMov(fila,columna)
                    if len(poliza) != 0:
                        sigMov = max(poliza)
                        if (sigMov[1] == 0):
                            Matrix[fila][columna] = 1
                            Matrix[fila-1][columna-1] = 2
                        elif sigMov[1] == 1:
                            Matrix[fila][columna] = 1
                            Matrix[fila-1][columna] = 2
                        elif sigMov[1] == 2:
                            Matrix[fila][columna] = 1
                            Matrix[fila-1][columna+1] = 2
                        elif sigMov[1] == 3:
                            Matrix[fila][columna] = 1
                            Matrix[fila][columna-1] = 2
                        elif sigMov[1] == 4:
                            Matrix[fila][columna+1] = 2
                            Matrix[fila][columna] = 1
                        elif sigMov[1] == 5:
                            Matrix[fila][columna] = 1
                            Matrix[fila+1][columna-1] = 2
                        elif sigMov[1] == 6:
                            Matrix[fila][columna] = 1
                            Matrix[fila+1][columna] = 2
                        elif sigMov[1] == 7:
                            Matrix[fila][columna] = 1
                            Matrix[fila+1][columna+1] = 2
                        elif sigMov[1] == 8:
                            Matrix[fila][columna] = 2

"""funcion que controla el semaforo sobre el cruce"""       
def semaforo():
    global sentido
    global Matrix
    
    if sentido == "WE":
        for columna in range (len(Matrix)):
            if 39<columna<60:
                Matrix[39][columna] = 4
                
    else:
        for columna in range (len(Matrix)):
            if 39<columna<60:
                Matrix[39][columna] = 1
                
    if sentido == "NS":
        for fila in range (len(Matrix)):
            if 39<fila<60:
                Matrix[fila][39] = 4
                
    else:
        for fila in range (len(Matrix)):
            if 39<fila<60:
                Matrix[fila][39] = 1
                
                
semaforo()    
   
"""
Loop que crea iteraciones infinitas del cruce
"""
on = 1 
while on == 1: 
    for n in range (100):
        norteSur(n)
        esteOeste(n)
                 
    np.savetxt('cruce.txt', Matrix, fmt='%d')
    iteracioneSemaf += 1
    
    """
    Fuzzy Logic tanto para los semáforos del cruce
    """
    
    #REVISION NS
    if(contAutosNs < 161):
        if(contAutosNs >= 81): 
            traficoNs = 'ligero: ', (80/float(contAutosNs)), ' medio: ', (1 - 80/float(contAutosNs)), " pesado: ", 0 
            if (iteracioneSemaf >= 5) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
                
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)    
        else:
            traficoNs = 'ligero: 1.0 - medio: 0 - pesado: 0'
            if (iteracioneSemaf >= 1) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)
    elif((contAutosNs >= 161) and (contAutosNs < 481)):
        if((contAutosNs >= 161) and (contAutosNs <= 241)):
            traficoNs = "ligero: ", 1-(float(contAutosNs-80)/160), ' medio: ', float(contAutosNs-80)/160, " pesado: 0"
            if (iteracioneSemaf >= 7) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)
        elif((contAutosNs > 241)  and (contAutosNs < 401)):
            traficoNs = 'ligero: 0, medio: 1, pesado: 0'
            if (iteracioneSemaf >= 9) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs) 
        elif ((contAutosNs >= 401) and (contAutosNs < 481)):
            traficoNs = 'ligero: 0 medio: ', 80/float(contAutosNs-320), ' pesado: ', 1 - 80/float(contAutosNs-320)
            if (iteracioneSemaf >= 11) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print( "traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)
    elif((contAutosNs >= 481) and (contAutosNs >= 800)):
        if ((contAutosNs >= 481) and (contAutosNs <= 560)):
            traficoNs = 'ligero: 0, medio: ', 1-float(contAutosNs-400)/160, ' pesado: ', float(contAutosNs-400)/160
            if ((iteracioneSemaf >= 13) and (sentido == "NS")):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)  
        elif 560 > contAutosNs:
            traficoNs = 'ligero: 0, medio: 0, pesado: 1'
            if (iteracioneSemaf >= 15) and (sentido == "NS"):
                sentido = "WE"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoNs: ", traficoNs, " contAutosNs: ", contAutosNs)
         
        
        
        
    #REVISION WE
    
    if(contAutosWe < 161):
        if (contAutosWe > 81): 
            traficoWe = 'ligero: ', 80/float(contAutosWe), ' medio: ', 1 - 80/float(contAutosWe), " pesado: ", 0 
            if (iteracioneSemaf >= 5) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe)   
        else:
            traficoWe = 'ligero: 1.0 - medio: 0 - pesado: 0'
            if (iteracioneSemaf >= 1) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe)     
    elif((contAutosWe >= 161) and (contAutosWe < 481)):
        if ((contAutosWe >= 161 ) and (contAutosWe <= 241)):
            traficoWe = "ligero: ", 1-float(contAutosWe-80)/160, ' medio: ', float(contAutosWe-80)/160, " pesado: 0"
            if (iteracioneSemaf >= 7) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe)  
        elif ((contAutosWe > 241) and (contAutosWe< 401)):
            traficoWe = 'ligero: 0, medio: 1, pesado: 0'
            if (iteracioneSemaf >= 9) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe) 
        elif ((contAutosWe >= 401) and (contAutosWe < 481)):
            traficoWe = 'ligero: 0 medio: ', 80/float(contAutosWe-320), ' pesado: ', 1 - 80/float(contAutosWe-320)
            if (iteracioneSemaf >= 11) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe)
    elif((contAutosWe >= 481) and (contAutosWe >= 800)):
        if ((contAutosWe >= 481) and (contAutosWe <= 560)):
            traficoWe = 'ligero: 0, medio: ', 1-float(contAutosWe-400)/160, ' pesado: ', float(contAutosWe-400)/160
            if (iteracioneSemaf >= 13) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe) 
        elif contAutosWe > 560:
            traficoWe = 'ligero: 0, medio: 0, pesado: 1'
            if (iteracioneSemaf >= 15) and (sentido == "WE"):
                sentido = "NS"
                semaforo()
                iteracioneSemaf = 0
               
                print("traficoWe: ", traficoWe, " contAutosWe: ", contAutosWe)

#plt.quiver( u, v, scale=2, units='xy')
#plt.show()





