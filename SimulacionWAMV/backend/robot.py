# Librerias Externas
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject

# Librerias Propias
import parametros as p
from backend.ente import SistemaDinamico

class RobotBrain (SistemaDinamico):

    def __init__ (self):
        # Load classes
        super ().__init__ (0, 'Robot', [20, 20, 30 * np.pi/16])

        # Agregar circulos
        self.add_volumen (3, 0, 0)
        self.add_volumen (1, 2, 2)
        self.add_volumen (1, -2, 2)
        