import numpy as np
from time import time
from os.path import join
import numpy.linalg as lg
from matplotlib import pyplot as plt

class Prognosis:

    def __init__ (self, iterations, simulation, density, max_time_sim=25,
                  show_graph=False, save_data=False, path_file=('test.txt')):
        
        self.iterations = iterations
        self.sim = simulation
        self.density = density
        self.max_time_sim = max_time_sim

        self.show_graph = show_graph
        self.save_data = save_data
        self.path_file = path_file

        self.storage_trayectors = []

    def run (self):
        """
        Esta funcion realiza la cantidad pedida de simulaciones
        luego determina la matriz de probabilidades y finalmente se determina
        las probabilidades para cada tiempo
        """
        start_time = time () 

        # Toma de trayectorias
        for _ in range (self.iterations):
            trayectory = self.sim.run ()

            # Save trayectory
            self.storage_trayectors.append (trayectory)

        # Determinar matriz de probabilidades
        self.prob_matrix ()

        # Calcular probabilidades
        data = self.pronostic ()

        # Detener tiempo
        end_time = time ()
        self.time_simulation = end_time - start_time

        if self.show_graph:
            plt.plot (range (1, len(data) + 1), data)
            plt.title (f'N = {self.iterations}' + r' $\sigma$' + '= 2')
            plt.xlabel ('Time (k)')
            plt.ylabel ('Probability')
            plt.show ()

        if self.save_data:
            # print(data)
            with open (self.path_file, 'w') as file:
                file.writelines (list(map(lambda x: str(x) +'\n', data)))

    def prob_matrix (self):
        """
        Esta funcion determina la matriz de probabilidad para no tener que
        calcular constantemente los valores de la probabilidad para cada trayectoria
        """
        # Esta sera una matriz de muestras x timepos en la muestras
        self.matrix_prob = np.zeros ((self.iterations, self.max_time_sim))

        for i in range (self.iterations):
            # i son las trayectorias
            for k in range (self.max_time_sim):
                # k son los tiempos
                self.matrix_prob[i, k] = self.density.pdf (*self.storage_trayectors[i][k])

    def probability_per_time (self, k):
        """
        Esta funcion determina la probabilidad de que la colision se 
        produzca en el tiempo k
        """
        sumatoria = 0 

        for i in range (self.iterations):
            # Con la matriz de porbabilidad
            pitatoria = self.matrix_prob[i, k]
            # Calculo directo
            # pitatoria = self.density.pdf (*self.storage_trayectors[i][k][:2])

            for j in range (1, k):
                # j = kp + 1 --> k - 1
                pitatoria *= (1 - self.matrix_prob[i, j])
                # pitatoria *= (1 - self.density.pdf (*self.storage_trayectors[i][j][:2]))

            sumatoria += pitatoria

        return sumatoria / self.iterations

    def pronostic (self):
        data = np.zeros ((self.max_time_sim, ))
        
        for k in range (1, self.max_time_sim):
            probability = self.probability_per_time (k)
            # print(probability)
            data[k] = probability

        # print("PRONOSTICO SUM:", sum(data))

        return data
            
class NearInstantaneous (Prognosis):

    def __init__ (self, density_step, *args, **kwargs):
        super().__init__ (*args, **kwargs)

        self.density_step = density_step

    def probability_per_time (self, k):
        sumatoria = 0 

        # Se recorren las trayectorias
        for i in range (self.iterations):
            V, m, R = self.compute_aux_vars (k - 1, i)

            # self.const_1 = sqrt (det(V) / (det(sigma_obs) * det(sigma_R)))

            # V^(-1) * m
            V_1_m = np.dot (lg.inv(V), m)

            pitatoria = self.const_1 * np.exp (- np.dot(m, V_1_m) + R)

            # for j in range (1, k - 1):
            #     # j = kp + 1 --> k - 1
            #     pitatoria *= (1 - self.matrix_prob[i, j])
            #     # pitatoria *= (1 - self.density.pdf (*self.storage_trayectors[i][j][:2]))

            print (pitatoria)
            sumatoria += pitatoria

        return sumatoria / self.iterations
    
    def pronostic (self):
        # Calcular algunas constates
        self.compute_const ()

        # Imprimiendo trayectorias
        for p in self.storage_trayectors[0]:
            print(f"({round(p[0], 1)}, {round(p[1], 1)})", end=' --> ')
        print("Fin de trayectorias")

        # Hacer el mismo procedimiento
        return super().pronostic ()
    
    def compute_const (self):
        # esta funcion servira para determinar valores constantes
        # V = sigma_obs^(-1) + sigma_R^(-1)
        self.V = lg.inv (self.density.cov) + lg.inv (self.density_step.cov)

        # sqrt (det(V) / (det(sigma_obs) * det(sigma_R)))
        self.const_1 = np.sqrt (lg.det (self.V) / (lg.det(self.density.cov) * lg.det (self.density_step.cov)))

        # sigma_obs^-1 * mu_obs
        self.const_2 = np.dot (lg.inv (self.density.cov), self.density.mean)

        # mu_obs^T * sigma_obs^-1 * mu_obs
        self.const_3 = np.dot (self.density.mean, self.const_2)

        # print (self.V)
        # print (self.const_1)
        # print (self.const_2)
        # print (self.const_3)
    
    def compute_aux_vars (self, k_1, i):
        # Computar las variables auxiliares para cada
        # tiempo k - 1 y trayectoria i
        mu_R = self.storage_trayectors[i][k_1]

        # V = sigma_obs^(-1) + sigma_R^(-1)
        V = self.V

        # sigma_R^(-1) * mu_R
        const_4 = np.dot(lg.inv(self.density_step.cov), mu_R)
        # m = sigma_obs^(-1) * mu_obs + sigma_R^(-1) * mu_R
        m = self.const_2 + const_4

        # R = mu_obs * sigma_obs^(-1) * mu_obs + mu_R * sigma_R^(-1) * mu_R
        R = self.const_3 + np.dot (mu_R, const_4)

        return V, m, R

        