import json
import math
import matplotlib.pyplot as plt
import numpy as np
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
        victima_circuito = 'qft5qu.py' # Nombre del fichero de la víctima
        for entrada in datos:
            # Normalizamos a minúsculas para evitar problemas de mayúsculas/minúsculas
            circuito = str(entrada.get('circuit_name', '')).lower()
            identificador = str(entrada.get('_id', '')).lower()
            
            if victima_circuito in circuito or 'qft' in identificador:
                return entrada['value']

        raise ValueError(
            f"No se encontro el resultado de la victima en {ruta_archivo}. "
            "Asegura que exista un documento con circuito Qft5Qu.py o _id que contenga 'qft'."
        )

def calcular_fidelidad_bhattacharyya(counts_ideal, counts_atacado, shots=10000):
    """Calcula el coeficiente de similitud entre distribuciones."""
    fidelidad = 0.0
    estados_posibles = set(list(counts_ideal.keys()) + list(counts_atacado.keys()))
    
    for estado in estados_posibles:
        prob_ideal = counts_ideal.get(estado, 0) / shots
        prob_atacado = counts_atacado.get(estado, 0) / shots
        fidelidad += math.sqrt(prob_ideal * prob_atacado)
        
    return fidelidad

# ==========================================
# 1. CARGA DE DATOS
# ==========================================
print("Cargando datos de los experimentos...")
counts_base = cargar_conteos('Victima/qft.json')
counts_ataque = cargar_conteos('Base/Perfil3/PerfilAlto3.json')
counts_mitigado = cargar_conteos('AislamientoTemporal/Perfil3/PerfilAlto3Aislamiento.json')


# ==========================================
# 2. CÁLCULO DE FIDELIDAD
# ==========================================
fid_ataque = calcular_fidelidad_bhattacharyya(counts_base, counts_ataque)
fid_mitigado = calcular_fidelidad_bhattacharyya(counts_base, counts_mitigado)

print("\n=== RESULTADOS DE MITIGACIÓN (AISLAMIENTO TEMPORAL) ===")
print(f"Fidelidad Ideal (Línea Base) : 100.00%")
print(f"Fidelidad bajo Ataque (Nivel 50): {fid_ataque * 100:.2f}%")
print(f"Fidelidad con Firewall (Delay)  : {fid_mitigado * 100:.2f}%")
print(f"-> ¡Recuperación de {(fid_mitigado - fid_ataque) * 100:.2f} puntos porcentuales!")

# ==========================================
# 3. GENERACIÓN DE GRÁFICA PARA EL PAPER
# ==========================================
# Elegimos 4 estados clave que demuestran la física del circuito
# 00000 y 11111 (Picos constructivos), 10001 y 01111 (Valles destructivos)
estados_clave = ['00000', '11111', '10001', '01111']

# Extraemos los valores para estos estados
valores_base = [counts_base.get(e, 0) for e in estados_clave]
valores_ataque = [counts_ataque.get(e, 0) for e in estados_clave]
valores_mitigado = [counts_mitigado.get(e, 0) for e in estados_clave]

# Configuración del gráfico
x = np.arange(len(estados_clave))
width = 0.25  # Ancho de las barras

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, valores_base, width, label='Línea Base (Ideal)', color='#2ca02c')
rects2 = ax.bar(x, valores_ataque, width, label='Ataque Carga Alta (Sin Defensa)', color='#d62728')
rects3 = ax.bar(x + width, valores_mitigado, width, label='Ataque Mitigado (QCRAFT Temporal)', color='#1f77b4')

# Etiquetas y formato académico
ax.set_ylabel('Conteos (Probabilidad)', fontsize=12)
ax.set_title('Impacto y Mitigación del Crosstalk en QFT (Estados Clave)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels([f"Estado $|{e}\\rangle$" for e in estados_clave], fontsize=11)
ax.legend(fontsize=11)

# Añadir una línea de "Ruido Blanco" de referencia (10000 shots / 32 estados = 312)
ax.axhline(y=312, color='gray', linestyle='--', alpha=0.7, label='Ruido Uniforme (Total Decoherencia)')
ax.legend()

plt.grid(axis='y', linestyle='--', alpha=0.5)

# Guardar y mostrar
plt.savefig('Comparacion_Mitigacion_Temporal.png', dpi=300, bbox_inches='tight')
print("\nGráfica guardada como 'Comparacion_Mitigacion_Temporal.png'")
plt.show()