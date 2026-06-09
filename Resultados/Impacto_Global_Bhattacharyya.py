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


def calcular_coeficiente_bhattacharyya(counts_ideal, counts_comparado):
    probs_ideal = normalizar_conteos(counts_ideal)
    probs_comparado = normalizar_conteos(counts_comparado)
    estados_posibles = set(probs_ideal.keys()) | set(probs_comparado.keys())

    coeficiente = 0.0
    for estado in estados_posibles:
        coeficiente += math.sqrt(probs_ideal.get(estado, 0.0) * probs_comparado.get(estado, 0.0))

    return coeficiente


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

    resultados = []
    for perfil, escenario, ruta in configuraciones:
        counts_comparado = cargar_conteos(ruta)
        coeficiente = calcular_coeficiente_bhattacharyya(counts_victima, counts_comparado)
        resultados.append((perfil, escenario, coeficiente))

    print('=== GLOBAL BHATTACHARYYA COEFFICIENT RESULTS ===')
    print('Ideal baseline (Victim vs Victim): 100.00%')
    for perfil, escenario, coeficiente in resultados:
        print(f'{perfil} - {escenario}: {coeficiente * 100:.2f}%')

    perfiles = ['Profile 1', 'Profile 2', 'Profile 3']
    escenarios = ['Low Load', 'High Load', 'Swarm']
    colores = ['#4C78A8', '#F58518', '#E45756']

    matriz = {perfil: {} for perfil in perfiles}
    for perfil, escenario, coeficiente in resultados:
        matriz[perfil][escenario] = coeficiente * 100.0

    valores_barras = [[matriz[perfil][escenario] for perfil in perfiles] for escenario in escenarios]

    x = np.arange(len(perfiles))
    width = 0.24

    fig, ax = plt.subplots(figsize=(11, 6.5))
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
        ax.bar_label(barras, fmt='%.1f%%', padding=3, fontsize=16)

    ax.set_ylim(0, 105)
    ax.set_ylabel('Bhattacharyya Coefficient (%)', fontsize=20)
    ax.set_xlabel('Profiles', fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(perfiles, fontsize=20)
    ax.grid(axis='y', linestyle='--', alpha=0.35)
    ax.legend(fontsize=20, ncol=2)

    plt.tight_layout()

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_salida = os.path.join(directorio_script, 'Impacto_Global_Bhattacharyya.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f'Chart saved as: {ruta_salida}')
    plt.show()


if __name__ == '__main__':
    main()
