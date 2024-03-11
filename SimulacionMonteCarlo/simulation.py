# Librerias Externas
from time import sleep
from random import randint

# Librerias Propias
from ente import SistemaDinamico
from visualizacion import Visual

class Simulacion:

    def __init__ (self, robot, objects=[], max_time_sim=50, end_sim='collision', show=0):

        self.robot = robot
        self.obs = objects
        self.max_time_sim = max_time_sim
        self.end_sim = end_sim
        self.show = show

        self.restart ()

        if self.show == 2:
            # Probar si funciona
            self.vision = Visual (self.robot.states_k, self.obs.states_k)

    def restart (self):
        self.loop = True
        self.time = 0

        # Reiniciar robot
        self.robot.restart ()

        # Reiniciar objetos
        for obs in self.obs:
            obs.restart ()

    def run (self):
        self.restart ()
        # while
        while self.loop:

            # actualizar tiemppo
            self.time += 1

            # calcular nueva posicion
            self.robot.update_pos ()

            # Visualizacion
            if self.show == 1:
                print (self.robot.states_k)
            elif self.show == 2:
                # hacerlo con interfaz
                # Probar si funciona
                self.vision.update (self.robot.states_k, self.obs.states_k)
                
            # Revisar finalizacion
            if self.is_finish ():
                return self.result
                
    def is_finish (self):
        if self.end_sim == 'collision':

            # detectar colision o final de la simulacion por cada objeto
            # terminar programa si es True
            for obs in self.obs:
                if self.robot.collision (obs):
                    return self.finish (self.save_time ())
                
            # Si el termino es tipo colision
            # Y aun no colision, verificar el tiempo de colision
            if self.robot.end_sim (self.max_time_sim):
                return self.finish (None)
            
        elif self.end_sim == 'time':
            # Si el termino es del tipo tiempo
            if self.time > self.max_time_sim:
                return self.finish (self.robot.trayectoria)
            
        else:
            # Aun no termina
            return False
        
    def finish (self, result):
        # Terminar simulacion
        self.loop = False

        # Guardar el resultado
        self.result = result

        # Decir que termino
        return True

    def save_time (self):
        if self.show == 1:
            print ("GAME OVER at", self.time, "seconds")

        return self.time
    
    def new_obs (self, caract, id_=None):
        id_ = id_ or randint(1, 1000)
        return SistemaDinamico (id_, f'OBS{id_}', caracts=caract)
    
    def add_obstacles (self, caract_obstacles):
        for obs in range(len(caract_obstacles)):
            new_obs = self.new_obs (caract_obstacles[obs], len(self.obs) + 1)

            self.obs.append (new_obs)
    
class S1 (Simulacion):
    # Simulacion para ver hasta que punto llega con un obstaculo
    def __init__ (self, caract_robot={}, caract_obs={}, **kwargs):
        
        # instanciar robot, obstaculo he interfaz
        robot = SistemaDinamico (0, 'ROBOT', caracts=caract_robot)

        super().__init__ (robot, **kwargs)

        # Agregar obstaculos
        self.add_obstacles (caract_obs)

class S2 (Simulacion):
    # Simulacion para ver cual es la trayectoria que alcanza hasta cierto tiempo

    def __init__(self, caract_robot={}, **kwargs):
        # Instanciar robot
        robot = SistemaDinamico (0, 'ROBOT', caracts=caract_robot)

        # Llamar a la clase padre
        super().__init__(robot, end_sim='time', **kwargs)
        

if __name__ == "__main__":
    from func import Sombrerito
    
    step_robot = Sombrerito (mu_x=1, mu_y=0, theta_x=0.5, theta_y=0.5)
    
    caract_robot = {
        'type': 'deterministic',
        'density step': step_robot,
        'initial': (0, 2)
    }

    sim = S1 (caract_robot ,end_sim='time')

    print (sim.run ())  

