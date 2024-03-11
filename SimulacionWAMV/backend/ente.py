# Librerias Externas
import numpy as np
from time import sleep
from random import random

from PyQt5.QtCore import pyqtSignal, QObject, QThread

# Librerias propias
import parametros as p

class SistemaDinamico (QThread):

    senal_instruction = pyqtSignal (dict)

    def __init__ (self, id_, name, x0):
        super ().__init__ ()

        # Nombre e identificacion
        self.name = name 
        self.id = id_

        # Estado del movimiento del sistema
        #                 x, y, theta
        self.states_k = x0

        # Maximo movimiento
        self.limit_v = p.ROBOT["v_k"]["LIMIT"]
        self.limit_nu = p.ROBOT["nu_k"]["LIMIT"]

        # Connect signals
        self.connect_signals ()

        # Representacion espacio
        self.volumen = []
        self.id_vol = 0

        # Loop
        self.loop = False

    def connect_signals (self):
        # Senales externas
        self.senal_instruction_manager = None
        self.senal_update_sim = None

        # Senales internas
        self.senal_instruction.connect (self.manage_instruction)
        
    def manage_instruction (self, info):
        
        if info["CMD"] == "UPDATE POS":
            # Enviar directo a sim
            for circulo in self.volumen:
                self.senal_update_sim.emit ({
                    "CMD": "UPDATE POS",
                    "ID": circulo.id,
                    "NAME": self.name,
                    "POS": circulo.pos,
                    "RADIO": circulo.radio
                })

            # Avisar al brain
            self.senal_instruction_manager.emit ({
                "CMD": "UPDATE POS",
                "ID": self.id
            })
        elif info["CMD"] == "START SIM":
            # Que empiece la simulacion
            self.start ()
        elif info["CMD"] == "STOP SIM":
            # Que empiece la simulacion
            self.stop ()

    def run (self):
        # Comenzar simulacion
        self.loop = True
        self.simulacion ()

    def stop (self):
        self.loop = False

    def simulacion (self):

        while self.loop:
            # print ("--- Nueva iteracion ---")
            update_pos = True
            # Calcular nuevos movimientos
            new_pos = self.new_pos (*self.states_k)
            # print (self.states_k, "-->", new_pos)
            
            # Revisar si alguno de los circulos queda afuera
            for circle in self.volumen:
                # Calcular nueva pos
                circle.new_pos (*new_pos)

                # Ver si choca con los limites
                if circle.colision_with_limits (next=1):
                    update_pos = False
                    break

            # Si y solo si los circulos estan dentro
            # se actualizan posiciones
            if update_pos:
                # Actualizarlos a las posiciones
                self.states_k = new_pos

                # Actualizar posiciones circulos
                for circle in self.volumen:
                    circle.update_pos ()

                # Actualizar widget
                self.senal_instruction.emit ({"CMD": "UPDATE POS"})

            # Esperar un tiempo
            sleep (p.Ts)

    def add_volumen (self, radio, x_r, y_r):
        # Crear volumen
        new_volumen = CirculoVolumen (self.id_vol, radio, x_r, y_r, *self.states_k)
        self.id_vol += 1

        # Asignar senales
        new_volumen.senal_instruction_manager = self.senal_instruction_manager

        # Agregar a la lista
        self.volumen.append (new_volumen)

    def new_pos (self, x, y, theta):
        # Calcular cambio del angulo
        delta_theta = random () * (self.limit_nu[1] - self.limit_nu[0]) + self.limit_nu[0] 
        # Calcular cambio de coordenadas
        delta = random () * self.limit_v[1]
        delta_x = delta * np.cos (theta + delta_theta)
        delta_y = delta * np.sin (theta + delta_theta)

        # Sumarlos a las posiciones
        new_x = x + delta_x
        new_y = y - delta_y
        new_theta = theta + delta_theta

        # theta
        new_theta = new_theta % (2 * np.pi)

        return [new_x, new_y, new_theta]
      
    def colision (self, other):
        # Si existe colision con alguno de los circulos
        for my_circle in self.volumen:
            for other_circle in other.volumen:

                if my_circle.colision_with_circle (other_circle):
                    return True

        # Si no colisiona con ninguno   
        return False
    
    def distancia (self, other):
        vect_dif = [self.states_k[0] - other.states_k[0], self.states_k[1] - other.states_k[1]]
        return np.linalg.norm (vect_dif)


class CirculoVolumen (QObject):

    senal_instruction = pyqtSignal (dict)

    def __init__ (self, id_, radio, x_rel, y_rel, x, y, theta):
        super ().__init__ ()

        # Identificacion
        self.id = id_

        # Geometria y posicion
        self.radio = radio
        self.pos_rel = [x_rel, y_rel]
        self.mag_pos_ref = np.linalg.norm (self.pos_rel)
        self.ang_pos_ref = np.arctan2 (*self.pos_rel)
        # Calcular la posicion actual
        self.new_pos (x, y, theta)
        # Actualizar la posicion
        self.update_pos ()

    def update_pos (self):        
        self.pos = self.next_pos

    def new_pos (self, x, y, theta):
        new_x = x + self.mag_pos_ref * np.cos (self.ang_pos_ref - theta)
        new_y = y + self.mag_pos_ref * np.sin (self.ang_pos_ref - theta)

        self.next_pos = [new_x, new_y]
        return new_x, new_y
    
    def colision (self, x, y):
        # Esta funcion determina si el punto entregado
        # Esta colicionando con el circulo
        x_act = self.pos[0]
        y_act = self.pos[1]

        vect_dif = [abs(x_act - x), abs(y_act - y)]

        if np.linalg.norm (vect_dif) < self.radio:
            return True
        
        return False
    
    def colision_with_circle (self, other):
        # Esta funcion determina si dos circulos 
        # estan colisionando
        vect_dif = np.array(self.pos) - np.array(other.pos)

        if np.linalg.norm (vect_dif) < self.radio + other.radio:
            return True
        
        return False
    
    def colision_with_limits (self, next=0):
        # Esta funcion determina si el circulo choca
        # con los limites o su posible colision en la siguiente
        # posicion
        # next = 0 => Se determina la colision actual
        # next = 1 => Se determina la posibilidad de colision

        if next == 0:
            pos = self.pos
        else:
            pos = self.next_pos
            # self.print_pos_vs_next ()

        # Revision eje x por izquierda
        vect_dif = [pos[0] - 0, 0]
        if np.linalg.norm (vect_dif) < self.radio:
            return True
        # Revision eje x por derecha
        vect_dif = [pos[0] - p.WIDTH_SIM / p.SCALE, 0]
        if np.linalg.norm (vect_dif) < self.radio:
            return True
        
        # Revision eje y por arriba
        vect_dif = [0, pos[1] - 0]
        if np.linalg.norm (vect_dif) < self.radio:
            return True
        # Revision eje y por abajo
        vect_dif = [0, pos[1] - p.HEIGHT_SIM / p.SCALE]
        if np.linalg.norm (vect_dif) < self.radio:
            return True
        
        return False
    
    def connect_signals (self):
        # Senales externas
        self.senal_instruction_manager = None

        # Senales internas
        self.senal_instruction.connect (self.manage_instruction)
        
    def manage_instruction (self, info):
        pass

    def print_pos_vs_next (self):
        print (self.id, ":", self.pos, "-->", self.next_pos, end=" | ")
        print (self.colision_with_limits (next=1))

    def __repr__ (self):
        return f"CIRCLE {self.id}"