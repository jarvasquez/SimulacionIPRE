import numpy as np
import seaborn as sns
from  time import time
from os.path import join
import matplotlib.pyplot as plt

import parametros as p

class MonteCarlo:

    def __init__ (self, iteration, simulation,
                  show_graph=False, save_data=False, path_file=('test.txt'),
                  max_failed_iteration=0, show_probability=False):
        self.N = iteration
        self.sim = simulation
        self.max_failed_iteration = max_failed_iteration
        self.failed_iteration = 0

        self.show_graph = show_graph
        self.save_data = save_data
        self.path_file = path_file
        self.show_probability = show_probability

        self.storage_dict = {}
        self.storage_list = []

    def run (self):
        start_time = time ()
        for _ in range(self.N):
            value = self.sim.run ()
            
            while value == None and self.failed_iteration < self.max_failed_iteration:
                value = self.sim.run ()

                self.failed_iteration += 1

            self.storage_list.append (value)

            if value == None:
                # Si se pasa del maximo de iteraciones fallidas debe evitar las demas
                continue

            if value in self.storage_dict.keys():
                self.storage_dict[value] += 1
            else:
                self.storage_dict[value] = 1

        end_time = time ()

        self.time_simulation = end_time - start_time
    
        if self.save_data:
            # Guardar en un archivo
            self.save ()
        if self.show_graph:
            # Mostrar el histograma
            self.show ()

    def save (self):
        # Sort storage
        with open(self.path_file, 'w') as file:
            file.writelines (list(map(lambda x: str(x) + '\n', self.storage_list)))

        # sort_storage = sorted(list((key, value) for key, value in self.storage_dict.items()))
        
        # with open (self.path_file, 'w') as file:
        #     file.write (f'Simultaitions: {self.N}')
        #     for key, value in sort_storage:
        #         file.write (f'{key}:{value}\n')

    def show (self):
        stat = "probability" if self.show_probability else "count"
        # Mostrar histograma [1]
        sns.histplot (x = np.array(self.storage_list), 
                      stat=stat, binrange=[p.SimParam.MIN_LIMIT_X, p.SimParam.MAX_LIMIT_X])
        plt.title (f'N = {self.N}')
        plt.xlabel ('Time (k)')

        plt.show ()

if __name__ == "__main__":
    from random import random

    class Random:

        def run (self):
            return random ()

    m = MonteCarlo (10, Random () , show_graph=True)
    m.run ()

# REFERENCIAS 
# [1] https://seaborn.pydata.org/generated/seaborn.histplot.html
