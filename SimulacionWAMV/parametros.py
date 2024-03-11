# Parametros de simulacion
Ts = 1 # En segundos
# Parametros del robot
ROBOT = {
    "v_k"   : {
        "LIMIT" : [0, 2]
    },
    "nu_k"  : {
        "LIMIT" : [-0.1, 0.1]
    }
}

# Parametros rutas guis
PATH_GUI = {
    'MAIN' : ("frontend", "gui", "MainW.ui"),
    'SIM' : ("frontend", "gui", "SimW.ui")
}

# Parametros interfaz
SCALE = 20
####################################
WIDTH_SIM = 1000
HEIGHT_SIM = 700
####################################