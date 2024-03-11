# Librerias Externas
from os.path import join

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout

# Librerias Propias
import parametros as p

# Cargamos el formulario creado en qt5-tools designer
windows_name, base_class = uic.loadUiType (join (*p.PATH_GUI["MAIN"]))

class MainWindow (windows_name, base_class):

    # Senales
    senal_update = pyqtSignal (dict)

    def __init__ (self):
        # Load classes
        super ().__init__ ()
        self.setupUi (self)

        # Some configurations
        self.init_gui ()

        # Connect signals
        self.connect_signals ()

        self.show ()

    def init_gui (self): 
        # Incluir layout para widget adicional
        self.layout = QVBoxLayout (self.centralwidget)

    def add_widget (self, new_widget):
        # This function add to the view the new window
        self.layout.addWidget (new_widget)

    def connect_signals (self):
        # Senales Internas
        self.senal_update.connect (self.manage_instruction)
        # Senales de acciones
        self.actionStart.triggered.connect (self.action_start)
        self.actionStop.triggered.connect (self.action_stop)

        # Senales externas
        self.senal_instruction_manager = None

    def manage_instruction (self, info):
        
        if info["CMD"] == "UPDATE STATUS BAR":
            self.statusBar().showMessage (info["MSG"])


    def action_start (self, s):
        self.senal_instruction_manager.emit ({"CMD": "START SIM"})

    def action_stop (self, s):
        self.senal_instruction_manager.emit ({"CMD": "STOP SIM"})


    