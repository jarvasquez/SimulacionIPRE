import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from func import Sombrerito
from simulation import S1, S2
from pronostico import Prognosis, NearInstantaneous
from monte_carlo import MonteCarlo
import parametros as p

def sim_montecarlo (N, max_time_sim, caract_robot, caract_obs, 
                    show_graph=True, save_data=False, name_file=('test.txt')):

    # Tipos de simulaciones 
    # deterministic = S1 ()
    gaussian = S1 (caract_robot, caract_obs, max_time_sim=max_time_sim)

    # Instancia de Montecarlo
    monte = MonteCarlo (N, gaussian, show_graph=show_graph, show_probability=True,
                        save_data=save_data, path_file=name_file)
    # Realizar simulacion
    monte.run ()

    # Algunos datos
    print ("\n------ MONTE CARLO ------")
    print ("Num Iterations:", N)
    print ("Simulation Time:", round(monte.time_simulation, 3), "seconds")
    # print ("Num of failed simulations:", monte.failed_iteration)

def sim_pronostico (N, max_time_sim, caract_robot, caract_obs, 
                    show_graph=True, save_data=False, name_file=('test.txt')):
    # Obtener todas las trayectorias
    # Determinar probabilidad de colision en tiempo k
    num_trayectorys = N

    sim = S2 (caract_robot, max_time_sim=max_time_sim)

    prog = Prognosis (num_trayectorys, sim, caract_obs[0]['density'],
                      show_graph=show_graph, max_time_sim=max_time_sim,
                      save_data=save_data, path_file=name_file)
    prog.run ()

    # Algunos datos
    print ("\n------ PRONOSTICO ------")
    print ("Num Trayectorys:", num_trayectorys)
    print ("Simulation Time:", round(prog.time_simulation, 3), "seconds")

def sim_near_instantaneus (N, max_time_sim, caract_robot, caract_obs):
    # Obtener todas las trayectorias
    # Determinar probabilidad de colision en tiempo k
    num_trayectorys = N

    sim = S2 (caract_robot, max_time_sim=max_time_sim)

    prog = NearInstantaneous (caract_robot['density step'], num_trayectorys, sim, caract_obs[0]['density'],               # Cambiar density
                              show_graph=True, max_time_sim=max_time_sim)
    prog.run ()

    # Algunos datos
    print ("\n------ NEAR INSTANTANEOUS ------")
    print ("Num Trayectorys:", num_trayectorys)
    print ("Simulation Time:", round(prog.time_simulation, 3), "seconds")
    
def save_datas (max_time_sim, caract_robot, caract_obs):
    # Ns = [int(1e3), int(1e4), int(1e5), int(1e6)]
    Ns = [int(1e2)]

    for n in Ns:
        # sim montecarlo
        sim_montecarlo (n, max_time_sim, caract_robot, caract_obs,
                        show_graph=False, save_data=True, name_file=f"historial/sim_monte_{n}.txt")

        # sim pronostic
        sim_pronostico (n, max_time_sim, caract_robot, caract_obs,
                        show_graph=False, save_data=True, name_file=f"historial/sim_prono_{n}.txt")

def view_data (N):
    print("Num Iterations:", N)
    # path_file_monte = f"historial/sim_monte_{N}.txt"
    path_file_monte = f"historial/sim_monte_1000.txt"
    path_file_prono = f"historial/sim_prono_{N}.txt"

    with open (path_file_monte, 'r') as file_monte:
        data_monte = file_monte.readlines ()
        print(data_monte.count('None\n')/N)
        data_monte = list(filter(lambda x: True if not 'None' in x else False, data_monte))
        data_monte = list(map(lambda x: int(x.strip()) if not 'None' in x else None, data_monte))
        frec_monte = [data_monte.count(i)/N for i in range(0, 20)]

        # print(frec_monte)
        # print(np.array(frec_monte) * N)

    with open (path_file_prono, 'r') as file_prono:
        data_prono = file_prono.readlines ()
        data_prono = list(map(lambda x: np.float64(x.strip ()), data_prono))
        
    # [1]
    # sns.histplot (x = data_monte, stat='probability', binrange=[p.SimParam.MIN_LIMIT_X, p.SimParam.MAX_LIMIT_X],
    #               label="Simulacion Monte Carlo", binwidth=1)
    plt.bar ([i for i in range(0, 20)], frec_monte, label="M1: Simulacion Monte Carlo")
    plt.title (f'N = {N}')
    plt.xlabel ('Time (k)')

    plt.plot (range (1, len(data_prono) + 1), data_prono, 
              color="red", label="M2: Pronostico")
    
    print(np.abs(np.array(frec_monte) - np.array(data_prono)).mean())

    plt.legend ()
    # plt.show ()
    

if __name__ == "__main__":  
    # Numero de iteraciones a realizar
    N = int(1e6)
    max_time_sim = p.SimParam.MAX_LIMIT_X # 20

    # Distribuciones
    density = Sombrerito (5, 2, 2, 2)
    step_robot = Sombrerito (mu_x=1, mu_y=0, theta_x=0.5, theta_y=0.01)
    
    # Caracteristicas robot y obstaculo
    caract_robot = {
        'type': 'deterministic',
        'density step': step_robot,
        'initial': (0, 2)
    }
    caract_obs = [
        {
            'type': 'gaussian',
            'density': density,
            'initial': (2, 2)
        }
    ]

    # Para realizar simulacion montecarlo
    # sim_montecarlo (N, max_time_sim, caract_robot, caract_obs)

    # Para realaizar simulacion por
    # sim_pronostico (N, max_time_sim, caract_robot, caract_obs)

    # SImulation casi isntantanea
    # sim_near_instantaneus (1, max_time_sim, caract_robot, caract_obs)

    # run all
    # save_datas (max_time_sim, caract_robot, caract_obs)

    # view data
    for n in [1e2, 1e3, 1e4, 1e5, 1e6]:
        view_data(int(n))
    # view_data (N)

# REFERENCIAS
# [1] multiplo graph plot https://learnt.io/blog/how-to-plot-multiple-graphs-in-python/