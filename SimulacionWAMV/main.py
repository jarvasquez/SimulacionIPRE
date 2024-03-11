# Librerias Externas
import sys
import numpy as np

# Librarias PyQt
from PyQt5.QtWidgets import QApplication

# Librerias Propias
from frontend.sim_window import SimWindow
from frontend.main_window import MainWindow

from backend.robot import RobotBrain
from backend.obstaculos import Obstaculo
from backend.manager import CentroOperaciones

def main ():
    # Iniciar Aplicacion
    app = QApplication([])

    # Iniciar frontend
    main_w = MainWindow ()
    sim_w = SimWindow ()

    # Agregar ventana especial
    main_w.add_widget (sim_w)

    # Iniciar backend
    management = CentroOperaciones ()
    robot = RobotBrain ()
    o1 = Obstaculo (1, [26.47, 20, np.pi])

    # Conectar senales
    # Centro con guis
    management.senal_update_main = main_w.senal_update
    management.senal_update_sim = sim_w.senal_update
    management.senal_update_sim_circle = sim_w.senal_update_circle
    # guis con backend
    main_w.senal_instruction_manager = management.senal_instruction

    # Connect signals to obstables and robot
    management.add_object (robot)
    management.add_object (o1)

    # Iniciar simulaciones
    management.senal_instruction.emit ({
        "CMD": "START"
    })

    # Salir del programa
    sys.exit (app.exec ())

if __name__ == "__main__":
    # Correr el programa
    main ()
    