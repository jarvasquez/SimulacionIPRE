# Librerias Externas
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject

# Librerias Propias
import parametros as p


class CentroOperaciones (QObject):

    senal_instruction = pyqtSignal (dict)

    def __init__ (self):
        super ().__init__ ()

        # Connect signals
        self.connect_signals ()

        # Guarda obstaculos y robot
        self.objects = dict ()

    def connect_signals (self):
        # Senales externas
        self.senal_update_main = None
        self.senal_update_sim = None
        self.senal_update_sim_circle = None

        # self.senal_instruction_robot = None
        self.senal_instruction_objects = dict ()

        # Senales internas
        self.senal_instruction.connect (self.manage_instruction)
        
    def manage_instruction (self, info):
        
        if info["CMD"] == "START":
            self.start (info)
        elif info["CMD"] == "START SIM":
            # Decir al robot que se mueva
            # self.senal_instruction_robot.emit (info)
            # Decir a los obstaculos que se muevan
            for senal in self.senal_instruction_objects.values ():
                senal.emit (info)
        elif info["CMD"] == "STOP SIM":
            # Decir al robot que se mueva
            # self.senal_instruction_robot.emit (info)
            # Decir a los obstaculos que se muevan
            for senal in self.senal_instruction_objects.values ():
                senal.emit (info)
        elif info["CMD"] == "UPDATE POS":
            # Posicion actualizada
            # Revisar colisiones
            self.review_colisions (info["ID"])

    def start (self, info):
        # Decir a robot que actualice su posicion
        # self.senal_instruction_robot.emit ({
        #     "CMD": "UPDATE POS"
        # })
        # Avisar a obstaculos
        for senal in self.senal_instruction_objects.values ():
            senal.emit ({"CMD": "UPDATE POS"})

    def add_object (self, new_object):
        # Relacionar senal
        self.senal_instruction_objects[new_object.id] = new_object.senal_instruction
        # Objecto con centro
        new_object.senal_instruction_manager = self.senal_instruction
        # Object with sim
        new_object.senal_update_sim = self.senal_update_sim_circle

        # Save object
        self.objects[new_object.id] = new_object

    def review_colisions (self, id_object_update):
        robot = self.objects[0]
        colision = False

        if id_object_update == 0:
            # El robot ha sido actualizado, revisar 
            # colision con el objeto mas cercano
            obs_cercano = self.objects[self.obs_cercano ()[0]]

            if robot.colision (obs_cercano):
                # Si el robot colisiona con obstaculo
                # Avisar 
                self.senal_update_main.emit ({
                    "CMD": "UPDATE STATUS BAR",
                    "MSG": "¡COLISION!"
                })
                colision = True
        else:
            # un obstaculo ha sido actualizado
            # revisar choque con robot
            obstaculo = self.objects [id_object_update]

            if obstaculo.colision (robot):
                # Si el robot colision con obstaculo
                # Avisar 
                self.senal_update_main.emit ({
                    "CMD": "UPDATE STATUS BAR",
                    "MSG": "¡COLISION!"
                })
                colision = True

        if not colision:
            # Si el robot no esta colisionando
            # avisar que no lo esta
            self.senal_update_main.emit ({
                "CMD": "UPDATE STATUS BAR",
                "MSG": ""
            })

    def obs_cercano (self):
        # Determina el obstaculo mas cercano a robot
        robot = self.objects[0]

        id_min_distancia = 1
        min_distancia = robot.distancia (self.objects[1])

        for id_ in self.objects.keys ():
            if id_ == 0:
                # es el robot
                continue
            else:
                # Es un obstaculo
                distancia_obs = robot.distancia (self.objects[id_])
                if distancia_obs < min_distancia:
                    id_min_distancia = id_
                    min_distancia = distancia_obs

        return id_min_distancia, min_distancia



