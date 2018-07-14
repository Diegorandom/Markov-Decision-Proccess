import numpy as np
from dataStructure import dataStructure


class DiscStructure(dataStructure):

    """
    - numStates: # estados
    - numAcciones: # acciones
    - transiciones: transiciones
    
    - dei: distribución del estado inicial es uniforme 
      transiciones[s][a] == [(probabilidad, sigEstado, recompensa, done)]
        list or array of length nS
        
    """
    def __init__(self, numStates, numAcciones, transiciones, dei):
        self.transiciones = transiciones
        self.dei = dei
        self.lastaction=None 
        self.numStates = numStates
        self.numAcciones = numAcciones

