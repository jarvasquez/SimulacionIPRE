# Librerias Externas
from os.path import join

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# Librerias Propias
import parametros as p

from frontend.circle import CircleLabel

# Cargamos el formulario creado en qt5-tools designer
windows_name, base_class = uic.loadUiType (join (*p.PATH_GUI["SIM"]))

class SimWindow (windows_name, base_class):

    # Senales
    senal_update = pyqtSignal (dict)
    senal_update_circle = pyqtSignal (dict)

    def __init__ (self):
        # Load classes
        super ().__init__ ()
        self.setupUi (self)

        # Fixe size
        self.setFixedSize (p.WIDTH_SIM, p.HEIGHT_SIM)

        # Connect signals
        self.connect_signals ()

        # Almacen de labels
        self.storage_circles = dict ()

        self.setFixedSize (p.WIDTH_SIM, p.HEIGHT_SIM)


    def connect_signals (self):
        # Senales Internas
        self.senal_update.connect (self.manage_instruction)
        self.senal_update_circle.connect (self.update_circle)

        # Senales externas

    def manage_instruction (self, info):
        pass

    def update_circle (self, info):
        
        if info["CMD"] == "UPDATE POS":
            if info["NAME"] in self.storage_circles:
                # Ya existe el robot u obstaculo en el almacen
                if info["ID"] in self.storage_circles[info["NAME"]]:
                    # Si existe en el storage, actualizarlo
                    circle = self.storage_circles[info["NAME"]][info["ID"]]

                    circle.update_pos (*info["POS"], info["RADIO"])
                else:
                    # Si no existe, crearlo
                    circle = CircleLabel (info["RADIO"], *info["POS"], info["NAME"], self)

                    self.storage_circles[info["NAME"]][info["ID"]] = circle
            else:
                # Agregar circulo
                circle = CircleLabel (info["RADIO"], *info["POS"], info["NAME"], self)

                # Agregar storage para robot u obstaculo con circulo inicial
                self.storage_circles[info["NAME"]] = {info["ID"] : circle}

            # print (self.storage_circles)



        # Se debe revisar siempre el tamano de la ventana
        # size_window = self.size ()
        # if size_window.width () != p.WIDTH_SIM:
        #     p.WIDTH_SIM = size_window.width ()
        # elif size_window.height () != p.HEIGHT_SIM:
        #     p.HEIGHT_SIM = size_window.height ()