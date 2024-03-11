# Librerias Externas
from os.path import join

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# Librerias Propias
import parametros as p

# Cargamos el formulario creado en qt5-tools designer
windows_name, base_class = uic.loadUiType (join (*p.PATH_GUI["SIM"]))

class TemplateWindow (windows_name, base_class):

    # Senales
    senal_update = pyqtSignal (dict)

    def __init__ (self):
        # Load classes
        super ().__init__ ()
        self.setupUi (self)

        # Connect signals
        self.connect_signals ()

    def connect_signals (self):
        # Senales Internas
        self.senal_update.connect (self.manage_instruction)

        # Senales externas

    def manage_instruction (self, info):
        pass