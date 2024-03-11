# Librerias Externas
import numpy as np

# Librerias Propias
import parametros as p
from backend.ente import SistemaDinamico

class Obstaculo (SistemaDinamico):

    def __init__ (self, id_, x0):
        # Load classes
        super ().__init__ (id_, f'Obstaculo {id_}', x0)

        # Agregar circulo
        self.add_volumen (3, 0, 0)