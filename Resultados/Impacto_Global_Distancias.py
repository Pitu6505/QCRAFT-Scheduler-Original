import json
import math
import os

import matplotlib.pyplot as plt
import numpy as np


def cargar_conteos(ruta_archivo):
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_script, ruta_archivo)

    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    if isinstance(datos, list) and len(datos) == 1:
        return datos[0]['value']

    victima_circuito = '/victima/qft5qu.py'
    for entrada in datos:
        circuito = str(entrada.get('circuit', '')).lower()
        identificador = str(entrada.get('_id', '')).lower()
        if victima_circuito in circuito or identificador == 'qft_victima' or 'qft' in identificador:
            return entrada['value']

    raise ValueError(
        f"No victim result was found in {ruta_archivo}. "
        "Make sure the JSON includes a document for Qft5Qu.py or _id QFT_Victima."
    )


def normalizar_conteos(conteos):
    total = sum(conteos.values())
    if total <= 0:
        raise ValueError('Counts cannot be empty or sum to zero.')
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


def extraer_soporte_y_probabilidades(conteos):
    total = sum(conteos.values())
    if total <= 0:
        raise ValueError('Counts cannot be empty or sum to zero.')

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
    soporte_ideal, probs_ideal = extraer_soporte_y_probabilidades(counts_ideal)
    soporte_atacado, probs_atacado = extraer_soporte_y_probabilidades(counts_atacado)

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


def main():
    counts_victima = cargar_conteos('Victima/qft.json')

    configuraciones = [
        ('Profile 1', 'Low Load', 'Base/Perfil1/PerfilBajo1.json'),
        ('Profile 1', 'High Load', 'Base/Perfil1/PerfilAlto1.json'),
        ('Profile 1', 'Swarm', 'Base/Perfil1/Enjambre.json'),
        ('Profile 2', 'Low Load', 'Base/Perfil2/PerfilBajo2.json'),
        ('Profile 2', 'High Load', 'Base/Perfil2/PerfilAlto2.json'),
        ('Profile 2', 'Swarm', 'Base/Perfil2/Enjambre2.json'),
        ('Profile 3', 'Low Load', 'Base/Perfil3/PerfilBajo3.json'),
        ('Profile 3', 'High Load', 'Base/Perfil3/PerfilAlto3.json'),
        ('Profile 3', 'Swarm', 'Base/Perfil3/Enjambre3.json'),
    ]

    resultados = {
        'Hellinger Distance': [],
        'Jensen-Shannon Distance': [],
        'Wasserstein Distance': [],
    }

    for perfil, escenario, ruta in configuraciones:
        counts_comparado = cargar_conteos(ruta)
        resultados['Hellinger Distance'].append((perfil, escenario, calcular_hellinger(counts_victima, counts_comparado)))
        resultados['Jensen-Shannon Distance'].append((perfil, escenario, calcular_jensen_shannon(counts_victima, counts_comparado)))
        resultados['Wasserstein Distance'].append((perfil, escenario, calcular_wasserstein(counts_victima, counts_comparado)))

    print('=== GLOBAL DISTANCE RESULTS ===')
    print('Ideal baseline (Victim vs Victim): 0.000000 for all distances')
    for metric_name, metric_results in resultados.items():
        print(f'\n--- {metric_name} ---')
        for perfil, escenario, valor in metric_results:
            print(f'{perfil} - {escenario}: {valor:.6f}')

    perfiles = ['Profile 1', 'Profile 2', 'Profile 3']
    escenarios = ['Low Load', 'High Load', 'Swarm']
    colores = ['#4C78A8', '#F58518', '#E45756']
    metricas = list(resultados.keys())

    matriz_metricas = {}
    for metric_name, metric_results in resultados.items():
        matriz = {perfil: {} for perfil in perfiles}
        for perfil, escenario, valor in metric_results:
            matriz[perfil][escenario] = valor
        matriz_metricas[metric_name] = matriz

    width = 0.24
    x = np.arange(len(perfiles))
    directorio_script = os.path.dirname(os.path.abspath(__file__))

    for metric_name in metricas:
        matriz = matriz_metricas[metric_name]
        valores_barras = [[matriz[perfil][escenario] for perfil in perfiles] for escenario in escenarios]

        fig, ax = plt.subplots(figsize=(11.5, 6.5))

        for idx, escenario in enumerate(escenarios):
            desplazamiento = (idx - 1) * width
            barras = ax.bar(
                x + desplazamiento,
                valores_barras[idx],
                width,
                label=escenario,
                color=colores[idx],
                edgecolor='black',
                linewidth=0.6,
            )
            ax.bar_label(barras, fmt='%.4f', padding=3, fontsize=16)

        ax.axhline(0, color='#222222', linestyle='--', linewidth=1.0, alpha=0.7)
        ax.set_ylabel(metric_name, fontsize=20)
        ax.set_xticks(x)
        ax.set_xticklabels(perfiles, fontsize=20)
        ax.set_xlabel('Profiles', fontsize=20)
        ax.grid(axis='y', linestyle='--', alpha=0.35)
        ax.legend(fontsize=20, ncol=3, loc='lower left')

        plt.tight_layout()

        file_suffix = metric_name.lower().replace(' ', '_').replace('-', '_')
        ruta_salida = os.path.join(directorio_script, f'Impacto_Global_{file_suffix}.png')
        plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        print(f'Chart saved as: {ruta_salida}')
        plt.show()
        plt.close(fig)


if __name__ == '__main__':
    main()
