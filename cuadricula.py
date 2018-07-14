import numpy as np
import discstructure
import sys
from io import StringIO



norte = 0
este = 1
sur = 2
oeste = 3
noreste = 4
noroeste = 5
sureste = 6
suroeste = 7

class Cuadricula(discstructure.DiscStructure):
    
    
    
    def __init__(self, dimensiones=[100,100]):
        """Si el objeto dimensiones no contiene listas o tuplas o si el largo de dimensiones es igual a 2 se debe lanzar un error con valor 2"""
        if not isinstance(dimensiones, (list, tuple)) or not len(dimensiones) == 2:
            raise ValueError('2')
            
        self.dimensiones = dimensiones
        
        """
        Documentación:
        
        Return the product of array elements over a given axis.
        
        axis : None or int or tuple of ints, optional

        Axis or axes along which a product is performed. The default, axis=None, will calculate the product of all the elements in the input array. If axis is negative it counts from the last to the first axis.

        New in version 1.7.0.

        If axis is a tuple of ints, a product is performed on all of the axes specified in the tuple instead of a single axis or all the axes as before.
        
        Explicación:
        
        numStates es un arreglo que contiene el producto de los elementos de el objeto dimensiones, sobre un eje determinado por las tuplas en todos los ejes determinados por estas tuplas.
        
        """
        numStates = np.prod(dimensiones)
        numAcciones = 8
        
        limiteY = dimensiones[0]
        limiteX = dimensiones[1]
        
        transiciones = {}
        
        """Values are generated within the half-open interval [start, stop) (in other words, the interval including start but excluding stop). For integer arguments the function is equivalent to the Python built-in range function, but returns an ndarray rather than a list."""
        cuadricula = np.arange(numStates).reshape(dimensiones)
        
        """
        NDITER
        Efficient multi-dimensional iterator object to iterate over arrays. To get started using this object, see the introductory guide to array iteration.
        
        “multi_index” causes a multi-index, or a tuple of indices with one per iteration dimension, to be tracked.
        “common_dtype” causes all the operands to be converted to a common data type, with copying or buffering as necessary.
        
        """
        
        iterador = np.nditer(cuadricula, flags=['multi_index'])
        
        
        """Iteración sobre los limitesY y X determinados por la posicion 0 y 1 respectivamente del objeto dimensiones. Dentro de esta iteracion podemos observar que si se sobrepasa los limites que corresponden a los carriles sobre los cuales los agentes se mueven, entonces una nueva posición en el arreglo movMalo con el valor de la coordenada de Y del movimiento multiplicada por 100 + i se agregará"""
        movMalo = []
        for q in range(limiteY):
            for w in range(limiteX):
                if(w<40 or w>60) and (q<40 or q>60):
                    movMalo.append((q*100)+w)
                    
        """En este caso la iteracion define aquellos lugares del mapa donde los movimientos son dificiles, estos son las banquetas. En caso de que se itere sobre un lugar determinado como lugar dificail el arreglo difMov agrega un nuevo valor determinado por (q*100)+w"""
        
        difMov = []
        for q in range(limiteY):
            for w in range(limiteX):
                if(w>39 and w<43 and w<61 and w>58)and(q<41 or q>58):
                    difMov.append((q*100)+w)
                if(q>39and q<43and q<61 and q>58) and (w<42 or q >58):
                    difMov.append((q*100)+w)
                    
                    
        """Arreglo extraído de referencia de código
        El arreglo meta y el arreglo obstaculo ambos tienen valores los cuales dado que la funcion de valor sea igual a estos valores significa que se ha llegado o a una meta o a un obstáculo
        
        """
        
        meta = [4199,4299,4399,4499,4699,4799,4899,4999,5199,5299,5399,5499,5699,5799,5899,
                5999,6099,9941,9942,9943,9944,9946,9947,9948,9949,9951,9952,9953,9954,9956,9957,9958,9959,9960]
                
        obstaculo = [4599,4598,4597,4596,4595,5099,5098,5097,5096,5095,5599,5598,5597,5596,5595,9945,9845,9745,9645,9545,9950,9850,9750,9650,9550,9955,9855,9755,9655,9555,
        4848,4846,4847,4849,4850,4851,4852,4853,4946,4947,4948,4949,4950,4951,4952,4953,5046,5047,5048,5049,5050,5051,5052,5053,
        5146,5147,5148,5149,5150,5151,5152,5153,4648,4649,4650,4651,4748,4749,4750,4751,5248,5249,5250,5251,5348,5349,5350,5351]
        
        contadorIteraciones = 0
        
        while not iterador.finished:
            indexIt = iterador.iterindex
            y, x = iterador.multi_index
            
            """Por cada indice de iteracion, una nueva posición del arreglo P = un arreglo vacio se crea con valor nA = 4
            
            
            """
            transiciones[indexIt] = {a : [] for a in range(numAcciones)}
            
            """
        
            Si el argumento que entre a estas funciones es igual a cualquiera de los valores del arreglo determinado (meta, movMalo, difMov y  obstaculo)
            
            """
            seTermino = lambda indexIt: indexIt in meta
            esMalMov = lambda indexIt: indexIt in movMalo
            esDifMov = lambda indexIt: indexIt in difMov
            esObstaculo = lambda indexit: indexIt in obstaculo
            
            if seTermino(indexIt):
                recompensa = 0.0
            elif esObstaculo(indexIt):
                recompensa = -50
            elif esDifMov(indexIt):
                recompensa = - 10
            elif esMalMov(indexIt):
                recompensa = -50
            else:
                recompensa = -1
                
                
            """En caso de haber terminado y pot lo tanto estar en la meta
                
                P[indexIt][acciones] == [(probabilidad, siguiente Estado, recompensa, terminado)]
            """
            if seTermino(indexIt):
                transiciones[indexIt][norte] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][este] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][sur] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][oeste] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][noreste] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][noroeste] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][sureste] = [(1.0, indexIt, recompensa, True)]
                transiciones[indexIt][suroeste] = [(1.0, indexIt, recompensa, True)]
            #En caso de no haber alcanzado la meta
            else:
                if y == 0 and x ==(limiteX-1):
                    dirNE = indexIt
                elif indexIt - limiteX + 1 < 10000:
                        dirNE= indexIt - limiteX + 1
                        
                if y == (limiteY - 1) and x == (limiteX - 1):
                    dirSE = indexIt
                elif indexIt + limiteX + 1 <10000:
                    dirSE = indexIt - limiteX + 1
                        
                if y == (limiteY - 1) and x == 0:
                    dirSO = indexIt
                elif indexIt + limiteX + 1 < 10000:
                    dirSO = indexIt - limiteX + 1
                    
                if x == 0 and y == 0:
                    dirNO = indexIt
                elif indexIt -limiteX -1 < 10000:
                    dirNO = indexIt - limiteX -1
                    
                if y == 0: 
                    dirN = indexIt 
                else: 
                    dirN = indexIt - limiteX
                    
                if x == (limiteX -1 ):
                    dirE = indexIt
                else:
                    dirE = indexIt+1
                    
                if y == (limiteY-1):
                    dirS = indexIt
                else: 
                    dirS= indexIt + limiteX
                
                if x == 0:
                    dirO = indexIt
                else:
                    dirO = indexIt - 1
                    
                transiciones[indexIt][norte] = [(1.0, dirN, recompensa, True)]
                transiciones[indexIt][este] = [(1.0, dirE, recompensa, True)]
                transiciones[indexIt][sur] = [(1.0, dirS, recompensa, True)]
                transiciones[indexIt][oeste] = [(1.0, dirO, recompensa, True)]
                transiciones[indexIt][noreste] = [(1.0, dirNE, recompensa, True)]
                transiciones[indexIt][noroeste] = [(1.0, dirNO, recompensa, True)]
                transiciones[indexIt][sureste] = [(1.0, dirSE, recompensa, True)]
                transiciones[indexIt][suroeste] = [(1.0, dirSO, recompensa, True)]
            
            contadorIteraciones = contadorIteraciones + 1
            iterador.iternext()
        else:
            print('El numero de iteraciones necesario fue:')
            print(contadorIteraciones)
            
        """La distribución del estado inicial es uniforme"""
        dei = np.ones(numStates)/numStates

        print("Se está calculando la poliza, al finalizar el proceso aparecerá una ventana con la función de valores, al cerrar esta ventana comenzarán a correr las iteraciones de la simulación del cruce")
        
        

        self.transiciones = transiciones

        super(Cuadricula, self).__init__(numStates, numAcciones, transiciones, dei)