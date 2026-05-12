import json
import math
import os

def cargar_conteos(ruta_archivo):
    # Obtener el directorio del script actual
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta absoluta
    ruta_completa = os.path.join(directorio_script, ruta_archivo)
    
    with open(ruta_completa, 'r') as f:
        datos = json.load(f)

        # Si el archivo tiene un unico resultado, lo devolvemos directamente.
        if isinstance(datos, list) and len(datos) == 1:
            return datos[0]['value']

        # Si hay resultados multiplexados, buscamos explicitamente el de la victima.
        victima_circuito = '/victima/qft5qu.py'
        for entrada in datos:
            circuito = str(entrada.get('circuit', '')).lower()
            identificador = str(entrada.get('_id', '')).lower()
            if victima_circuito in circuito or identificador == 'qft_victima':
                return entrada['value']

        raise ValueError(
            f"No se encontro el resultado de la victima en {ruta_archivo}. "
            "Asegura que exista un documento con circuito Qft5Qu.py o _id QFT_Victima."
        )

def calcular_fidelidad_bhattacharyya(counts_ideal, counts_atacado, shots=10000):
    fidelidad = 0.0
    estados_posibles = set(list(counts_ideal.keys()) + list(counts_atacado.keys()))
    
    for estado in estados_posibles:
        prob_ideal = counts_ideal.get(estado, 0) / shots
        prob_atacado = counts_atacado.get(estado, 0) / shots
        fidelidad += math.sqrt(prob_ideal * prob_atacado)
        
    return fidelidad

# 1. Cargar los resultados
counts_base = cargar_conteos('Victima/qft.json')
counts_bajo = cargar_conteos('Perfil1/PerfilBajo1.json')
counts_alto = cargar_conteos('Perfil1/PerfilAlto1.json')
counts_enjambre = cargar_conteos('Perfil1/Enjambre.json')

# 2. Calcular fidelidades respecto a la línea base
fid_bajo = calcular_fidelidad_bhattacharyya(counts_base, counts_bajo)
fid_alto = calcular_fidelidad_bhattacharyya(counts_base, counts_alto)
fid_enjambre = calcular_fidelidad_bhattacharyya(counts_base, counts_enjambre)

# 3. Mostrar resultados para el paper
print("=== RESULTADOS DEL ATAQUE DE CROSSTALK (PERFIL 1) ===")
print(f"Fidelidad Línea Base    : 100.00%")
print(f"Fidelidad Carga Baja    : {fid_bajo * 100:.2f}%")
print(f"Fidelidad Carga Alta    : {fid_alto * 100:.2f}%")
print(f"Fidelidad Enjambre      : {fid_enjambre * 100:.2f}%")