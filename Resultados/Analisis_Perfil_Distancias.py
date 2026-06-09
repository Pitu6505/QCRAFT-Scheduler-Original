import json
import math
import os


def cargar_conteos(ruta_archivo):
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_script, ruta_archivo)

    with open(ruta_completa, 'r') as archivo:
        datos = json.load(archivo)

        if isinstance(datos, list) and len(datos) == 1:
            return datos[0]['value']

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


def normalizar_conteos(conteos):
    total = sum(conteos.values())
    if total <= 0:
        raise ValueError('Los conteos no pueden estar vacios o sumar cero.')
    return {estado: valor / total for estado, valor in conteos.items()}


def calcular_hellinger(counts_ideal, counts_atacado):
    probs_ideal = normalizar_conteos(counts_ideal)
    probs_atacado = normalizar_conteos(counts_atacado)
    estados_posibles = set(probs_ideal.keys()) | set(probs_atacado.keys())

    suma = 0.0
    for estado in estados_posibles:
        raiz_ideal = math.sqrt(probs_ideal.get(estado, 0.0))
        raiz_atacado = math.sqrt(probs_atacado.get(estado, 0.0))
        suma += (raiz_ideal - raiz_atacado) ** 2

    return math.sqrt(suma) / math.sqrt(2.0)


def calcular_jensen_shannon(counts_ideal, counts_atacado):
    probs_ideal = normalizar_conteos(counts_ideal)
    probs_atacado = normalizar_conteos(counts_atacado)
    estados_posibles = set(probs_ideal.keys()) | set(probs_atacado.keys())

    divergence = 0.0
    for estado in estados_posibles:
        p = probs_ideal.get(estado, 0.0)
        q = probs_atacado.get(estado, 0.0)
        m = 0.5 * (p + q)

        if p > 0 and m > 0:
            divergence += 0.5 * p * math.log2(p / m)
        if q > 0 and m > 0:
            divergence += 0.5 * q * math.log2(q / m)

    return math.sqrt(divergence)


def _extraer_soporte_y_probabilidades(conteos):
    total = sum(conteos.values())
    if total <= 0:
        raise ValueError('Los conteos no pueden estar vacios o sumar cero.')

    soporte = []
    probabilidades = []
    for estado, valor in conteos.items():
        soporte.append(int(estado, 2))
        probabilidades.append(valor / total)

    ordenados = sorted(zip(soporte, probabilidades), key=lambda elemento: elemento[0])
    soporte_ordenado = [valor for valor, _ in ordenados]
    probabilidades_ordenadas = [valor for _, valor in ordenados]
    return soporte_ordenado, probabilidades_ordenadas


def calcular_wasserstein(counts_ideal, counts_atacado):
    soporte_ideal, probs_ideal = _extraer_soporte_y_probabilidades(counts_ideal)
    soporte_atacado, probs_atacado = _extraer_soporte_y_probabilidades(counts_atacado)

    estados = sorted(set(soporte_ideal) | set(soporte_atacado))
    indice_ideal = {estado: idx for idx, estado in enumerate(soporte_ideal)}
    indice_atacado = {estado: idx for idx, estado in enumerate(soporte_atacado)}

    acumulada_ideal = 0.0
    acumulada_atacada = 0.0
    distancia = 0.0
    anterior = estados[0]

    for estado in estados:
        distancia += abs(acumulada_ideal - acumulada_atacada) * (estado - anterior)

        if estado in indice_ideal:
            acumulada_ideal += probs_ideal[indice_ideal[estado]]
        if estado in indice_atacado:
            acumulada_atacada += probs_atacado[indice_atacado[estado]]

        anterior = estado

    return distancia


def mostrar_resultados(nombre, counts_base, counts_comparado):
    hellinger = calcular_hellinger(counts_base, counts_comparado)
    jensen_shannon = calcular_jensen_shannon(counts_base, counts_comparado)
    wasserstein = calcular_wasserstein(counts_base, counts_comparado)

    print(f"\n--- {nombre} ---")
    print(f"Distancia de Hellinger       : {hellinger:.6f}")
    print(f"Distancia de Jensen-Shannon  : {jensen_shannon:.6f}")
    print(f"Distancia de Wasserstein     : {wasserstein:.6f}")


def main():
    counts_base = cargar_conteos('Victima/qft.json')
    counts_bajo = cargar_conteos('Base/Perfil3/PerfilBajo3.json')
    counts_alto = cargar_conteos('Base/Perfil3/PerfilAlto3.json')
    counts_enjambre = cargar_conteos('Base/Perfil3/Enjambre3.json')

    print('=== RESULTADOS DEL ATAQUE DE CROSSTALK (PERFIL 3) ===')
    print('Comparacion de distribuciones con respecto a la linea base')

    print('\n--- Linea Base ---')
    print('Distancia de Hellinger       : 0.000000')
    print('Distancia de Jensen-Shannon  : 0.000000')
    print('Distancia de Wasserstein     : 0.000000')

    mostrar_resultados('Carga Baja', counts_base, counts_bajo)
    mostrar_resultados('Carga Alta', counts_base, counts_alto)
    mostrar_resultados('Enjambre', counts_base, counts_enjambre)


if __name__ == '__main__':
    main()