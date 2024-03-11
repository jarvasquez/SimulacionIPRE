# Librerias Externas
from os.path import join

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt

# Librerias Propias
import parametros as p

class CircleLabel (QLabel):

    # Senales
    senal_update = pyqtSignal (dict)

    def __init__ (self, radio, x, y, *args):
        # Load classes
        super ().__init__ (*args)

        # Iniciar gui
        self.init_gui (radio, x, y)

        # Connect signals
        self.connect_signals ()

    def init_gui (self, radio, x, y):
        # Actualizar pos
        self.update_pos (x, y, radio)

        # Centrar Texto
        self.setAlignment (Qt.AlignCenter)

        # setear radio como tamano circulo
        r_px =  int(radio) * p.SCALE

        # making label square in size
        # Se setea el largo y ancho
        self.resize(r_px * 2, r_px * 2)
 
        # setting up border and radius
        # Se setea el color y el radio
        self.setStyleSheet("border: 3px solid blue;"
                            + f"border-radius: {r_px}px;")

    def connect_signals (self):
        # Senales Internas
        self.senal_update.connect (self.manage_instruction)

        # Senales externas

    def manage_instruction (self, info):
        pass
    
    def update_pos (self, x, y, radio):
        self.move ((x - radio) * p.SCALE, (y - radio) * p.SCALE)

    def __repr__ (self):
        return "Circle"