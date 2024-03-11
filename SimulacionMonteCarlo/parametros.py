class SimParam:

    # Parametros de simulacion
    # Periodo de muestreo
    Ts = 0.1

    # Limites
    MAX_LIMIT_Y = 5
    MIN_LIMIT_Y = 0
    MAX_LIMIT_X = 20
    MIN_LIMIT_X = 0

    # Variables aleatorias
    DECIMALES = 1
    
    # Puede ser cualquier valor
    RANDOM_UPPER_Y = 4
    RANDOM_LOWER_Y = -4
    # Solo puede avanzar
    RANDOM_UPPER_X = 4
    RANDOM_LOWER_X = -4

class View:
    # Periodo muestre
    Ts = 0.5

    # Limites graph
    MAX_LIMIT_Y = SimParam.MAX_LIMIT_Y
    MIN_LIMIT_Y = SimParam.MIN_LIMIT_Y
    MAX_LIMIT_X = SimParam.MAX_LIMIT_X
    MIN_LIMIT_X = SimParam.MIN_LIMIT_X