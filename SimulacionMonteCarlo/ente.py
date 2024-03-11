# Librerias Externas
from hmac import new
from networkx import density
import numpy as np
from time import sleep
from scipy.stats import norm
from random import random, seed

# Librerias Propias
from parametros import SimParam

class SistemaDinamico:

    def __init__ (self, id_, name, caracts, bool_seed=False):
        # Nombre e identificacion
        self.name = name 
        self.id = id_

        # Densidad de probabilidad
        if 'density' in caracts.keys ():
            self.density = caracts['density']
        else:
            self.density = None

        # Densidad de probabilidad del movimiento
        if 'density step' in caracts.keys ():
            self.density_step = caracts['density step']
        else:
            self.density_step = None

        # Estado del movimiento del sistema
        #                 x, y
        if 'initial' in caracts.keys ():
            self.states_k = np.array(caracts['initial'])
            self.states_0 = np.array(caracts['initial'])
        else:
            self.states_k = np.array((0, 0))
            self.states_0 = np.array((0, 0))

        self.trayectoria = []

        # Tipo de movimiento
        if 'type' in caracts.keys ():
            self.tipo = caracts['type']
        else:
            self.tipo = 'deterministic'
        # Opciones
        #   deterministic: el objeto se sabe con certeza donde esta
        #   gaussian: el objeto es gaussianamente incierto

        if bool_seed:
            # Para hacer siempre la misma prediccion
            seed (1)

    def restart (self):
        self.states_k = self.states_0
        self.trayectoria = []

    def begin_sim (self):
        # Comenzar el programa
        self.loop = True
        self.run ()

    def stop_sim (self):
        self.loop = False

    def run (self):
        while self.loop:
            # Calcular nuevos movimientos
            new_pos = self.new_pos (self.states_k)
            # print (self.states_k, "-->", new_pos)

            # Actualizarlos a las posiciones
            self.states_k = new_pos

            # Esperar un tiempo
            sleep (SimParam.Ts)
            
    def new_pos (self, state):
        # Nuevo delta
        deltas = self.random (SimParam.DECIMALES)
        # print(deltas)

        # Calculos aleatorios
        new_state = state + deltas

        # Aplicar limites
        # new_x = self.limit_new_pos (new_x, SimParam.MAX_LIMIT_X, SimParam.MIN_LIMIT_X)
        # new_y = self.limit_new_pos (new_y, SimParam.MAX_LIMIT_Y, SimParam.MIN_LIMIT_Y)

        return np.array(new_state)
    
    def update_pos (self):
        # Determinar nueva pos
        new_pos = self.new_pos (self.states_k)

        # Guardar en trayectoria
        self.trayectoria.append (self.states_k)

        # Actualizar pos
        self.states_k = new_pos
    
    def random (self, decimals):
        if self.density_step != None:
            # Si el sistema tiene una densidad
            new_number = self.density_step.rvs ()
            # print(new_number)
        else:
            # Si no tiene mandar aleatoriedad uniforme
            new_number = []

            for _ in range(len(self.states_k)):
                new_number.append (random())

        return np.array(list(map(lambda x: round (x, decimals), new_number)))
    
    def limit_new_pos (self, pos, upper, lower):
        if pos > upper:
            return upper
        elif pos < lower:
            return lower 
        
        return pos
    
    def collision (self, other):

        if other.tipo == 'deterministic':
            if self.states_k[0] == other.states_k[0] and self.states_k[1] == other.states_k[1]:
                return True
        elif other.tipo == 'gaussian':
            # Teniendo la posicion del robot
            # evaluar la probabilidad de colision
            prob_collision = other.prob_collision (self.states_k)
            # luego tirar la moneda
            # print (self.states_k, other.states_k, prob_collision)
            
            random_number = random ()

            if prob_collision > random_number:
                # print ("Colisiona con probabilidad", prob_collision, random_number)
                return True
        
        return False
    
    def prob_collision (self, states_other):

        if self.density == None:
            # [1]
            # norm crea una distribucion normal con
            # loc: average
            # scale: standard desviation
            # cdf esntrega la probabilidad
            prob_x = norm (loc=self.states_k[0], scale=2).pdf (states_other[0])
            prob_y = norm (loc=self.states_k[1], scale=2).pdf (states_other[1])

            # Como son eventos independientes 
            # su probabilidad conjunta es solo multiplicada
            return prob_x * prob_y
        else:
            return self.density.pdf (*states_other)
    
    def end_sim (self, max_time_sim):
        if self.states_k[0] >= max_time_sim:
            return True
        
        return False

# REFERENCIAS
# [1] Norm Distribution https://www.askpython.com/python/normal-distribution
