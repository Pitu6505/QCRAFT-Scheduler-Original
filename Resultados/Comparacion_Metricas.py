import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.spatial.distance import jensenshannon
from scipy.stats import wasserstein_distance

def cargar_conteos(ruta_archivo):
    """
    Carga los conteos de un archivo JSON.
    Si hay múltiples resultados, busca el de la víctima.
    """
    # Obtener el directorio del script actual
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta absoluta
    ruta_completa = os.path.join(directorio_script, ruta_archivo)
    
    with open(ruta_completa, 'r') as f:
        datos = json.load(f)

        # Si el archivo tiene un único resultado, lo devolvemos directamente.
        if isinstance(datos, list) and len(datos) == 1:
            return datos[0]['value']

        # Si hay resultados multiplexados, buscamos explícitamente el de la víctima.
        victima_circuito = 'qft5qu.py'  # Nombre del fichero de la víctima
        for entrada in datos:
            # Normalizamos a minúsculas para evitar problemas de mayúsculas/minúsculas
            circuito = str(entrada.get('circuit_name', '')).lower()
            identificador = str(entrada.get('_id', '')).lower()
            
            if victima_circuito in circuito or 'qft' in identificador:
                return entrada['value']

        raise ValueError(
            f"No se encontró el resultado de la víctima en {ruta_archivo}. "
            "Asegura que exista un documento con circuito Qft5Qu.py o _id que contenga 'qft'."
        )


# ==========================================
# MÉTRICAS DE SIMILITUD/DISTANCIA
# ==========================================

def calcular_fidelidad_bhattacharyya(counts_ideal, counts_atacado, shots=10000):
    """Calcula el coeficiente de Bhattacharyya (similitud)."""
    fidelidad = 0.0
    estados_posibles = set(list(counts_ideal.keys()) + list(counts_atacado.keys()))
    
    for estado in estados_posibles:
        prob_ideal = counts_ideal.get(estado, 0) / shots
        prob_atacado = counts_atacado.get(estado, 0) / shots
        fidelidad += math.sqrt(prob_ideal * prob_atacado)
        
    return fidelidad


def calcular_distancia_hellinger(counts_ideal, counts_atacado, shots=10000):
    """
    Calcula la distancia de Hellinger entre dos distribuciones.
    Rango: [0, 1], donde 0 = idénticas, 1 = completamente diferentes.
    """
    estados_posibles = set(list(counts_ideal.keys()) + list(counts_atacado.keys()))
    suma_raices = 0.0
    
    for estado in estados_posibles:
        prob_ideal = counts_ideal.get(estado, 0) / shots
        prob_atacado = counts_atacado.get(estado, 0) / shots
        suma_raices += (math.sqrt(prob_ideal) - math.sqrt(prob_atacado)) ** 2
    
    # Distancia de Hellinger: sqrt(suma / 2)
    distancia = math.sqrt(suma_raices / 2.0)
    
    # Convertir a similitud: 1 - distancia
    return 1.0 - distancia


def calcular_divergencia_jensen_shannon(counts_ideal, counts_atacado, shots=10000):
    """
    Calcula la divergencia Jensen-Shannon entre dos distribuciones.
    Rango: [0, log(2)], métrica simétrica basada en KL.
    Aquí convertimos a similitud: 1 - JS_divergence / log(2)
    """
    estados_posibles = sorted(set(list(counts_ideal.keys()) + list(counts_atacado.keys())))
    
    # Convertir a vectores de probabilidad
    probs_ideal = np.array([counts_ideal.get(e, 0) / shots for e in estados_posibles])
    probs_atacado = np.array([counts_atacado.get(e, 0) / shots for e in estados_posibles])
    
    # Calcular divergencia Jensen-Shannon
    js_divergencia = jensenshannon(probs_ideal, probs_atacado)
    
    # Convertir a similitud: 1 - (JS / log(2))
    similitud = 1.0 - (js_divergencia / math.log(2))
    
    return similitud


def calcular_distancia_wasserstein(counts_ideal, counts_atacado, shots=10000):
    """
    Calcula la distancia de Wasserstein (Earth Mover's Distance) entre dos distribuciones.
    Mide el costo mínimo de transportar una distribución a otra.
    Rango: [0, 1] (normalizada), donde 0 = idénticas.
    Aquí convertimos a similitud: 1 - distancia_normalizada
    """
    estados_posibles = sorted(set(list(counts_ideal.keys()) + list(counts_atacado.keys())))
    
    # Mapear estados a índices numéricos (suponiendo estados binarios)
    # Para estados como '00000', convertimos a índice en [0, 2^n)
    indices = {}
    for i, estado in enumerate(estados_posibles):
        indices[estado] = i
    
    # Crear vectores de probabilidad
    probs_ideal = np.array([counts_ideal.get(e, 0) / shots for e in estados_posibles])
    probs_atacado = np.array([counts_atacado.get(e, 0) / shots for e in estados_posibles])
    
    # Crear matriz de posiciones (distancia entre estados)
    # Para simplicidad, usamos la distancia de Hamming normalizada
    u = np.arange(len(estados_posibles))
    
    # Calcular distancia de Wasserstein normalizada
    distancia_wass = wasserstein_distance(u, u, probs_ideal, probs_atacado)
    
    # Normalizar por la máxima distancia posible
    max_distancia = len(estados_posibles) - 1
    if max_distancia > 0:
        distancia_normalizada = distancia_wass / max_distancia
    else:
        distancia_normalizada = 0.0
    
    # Convertir a similitud
    return 1.0 - distancia_normalizada


# ==========================================
# 1. CARGA DE DATOS
# ==========================================
print("=" * 60)
print("Cargando datos de los experimentos...")
print("=" * 60)

# TODO: Cambiar estas rutas según tus archivos JSON
counts_base = cargar_conteos('Victima/qft.json')
counts_ataque = cargar_conteos('Base/Perfil3/PerfilAlto3.json')
counts_mitigado = cargar_conteos('CompilacionAleatoria/Perfil3/PerfilAlto3Desa.json')

print("✓ Datos cargados correctamente\n")

# ==========================================
# 2. CÁLCULO DE MÉTRICAS
# ==========================================
print("Calculando métricas...")
print("-" * 60)

# Bhattacharyya (referencia)
fid_bhatt_ataque = calcular_fidelidad_bhattacharyya(counts_base, counts_ataque)
fid_bhatt_mitigado = calcular_fidelidad_bhattacharyya(counts_base, counts_mitigado)

# Hellinger
sim_hellinger_ataque = calcular_distancia_hellinger(counts_base, counts_ataque)
sim_hellinger_mitigado = calcular_distancia_hellinger(counts_base, counts_mitigado)
dist_hellinger_ataque = 1.0 - sim_hellinger_ataque
dist_hellinger_mitigado = 1.0 - sim_hellinger_mitigado

# Jensen-Shannon
sim_js_ataque = calcular_divergencia_jensen_shannon(counts_base, counts_ataque)
sim_js_mitigado = calcular_divergencia_jensen_shannon(counts_base, counts_mitigado)
dist_js_ataque = 1.0 - sim_js_ataque
dist_js_mitigado = 1.0 - sim_js_mitigado

# Wasserstein
sim_wass_ataque = calcular_distancia_wasserstein(counts_base, counts_ataque)
sim_wass_mitigado = calcular_distancia_wasserstein(counts_base, counts_mitigado)
dist_wass_ataque = 1.0 - sim_wass_ataque
dist_wass_mitigado = 1.0 - sim_wass_mitigado

# ==========================================
# 3. MOSTRAR RESULTADOS
# ==========================================
print("\n" + "=" * 60)
print("RESULTADOS DE MITIGACIÓN (Aislamiento Temporal)")
print("=" * 60)

print("\n┌─ MÉTRICA: BHATTACHARYYA (Similitud) ─────────────────┐")
print(f"│ Línea Base (Ideal)          : 100.00%                 │")
print(f"│ Bajo Ataque                 : {fid_bhatt_ataque * 100:6.2f}%                 │")
print(f"│ Con Aislamiento Temporal    : {fid_bhatt_mitigado * 100:6.2f}%                 │")
print(f"│ → Recuperación              : +{(fid_bhatt_mitigado - fid_bhatt_ataque) * 100:5.2f} pp                │")
print("└───────────────────────────────────────────────────────┘")

print("\n┌─ MÉTRICA: HELLINGER (Similitud) ──────────────────────┐")
print(f"│ Línea Base (Ideal)          : 100.00%                 │")
print(f"│ Bajo Ataque                 : {sim_hellinger_ataque * 100:6.2f}%                 │")
print(f"│ Con Aislamiento Temporal    : {sim_hellinger_mitigado * 100:6.2f}%                 │")
print(f"│ → Recuperación              : +{(sim_hellinger_mitigado - sim_hellinger_ataque) * 100:5.2f} pp                │")
print("└───────────────────────────────────────────────────────┘")

print("\n┌─ MÉTRICA: JENSEN-SHANNON (Similitud) ──────────────────┐")
print(f"│ Línea Base (Ideal)          : 100.00%                  │")
print(f"│ Bajo Ataque                 : {sim_js_ataque * 100:6.2f}%                  │")
print(f"│ Con Aislamiento Temporal    : {sim_js_mitigado * 100:6.2f}%                  │")
print(f"│ → Recuperación              : +{(sim_js_mitigado - sim_js_ataque) * 100:5.2f} pp                 │")
print("└────────────────────────────────────────────────────────┘")

print("\n┌─ MÉTRICA: WASSERSTEIN (Similitud) ─────────────────────┐")
print(f"│ Línea Base (Ideal)          : 100.00%                 │")
print(f"│ Bajo Ataque                 : {sim_wass_ataque * 100:6.2f}%                 │")
print(f"│ Con Aislamiento Temporal    : {sim_wass_mitigado * 100:6.2f}%                 │")
print(f"│ → Recuperación              : +{(sim_wass_mitigado - sim_wass_ataque) * 100:5.2f} pp                │")
print("└───────────────────────────────────────────────────────┘")

print("\n" + "=" * 60)
print("VALORES NUMÉRICOS BRUTOS DE CADA MÉTRICA")
print("=" * 60)
print(f"Bhattacharyya coef.  ataque   : {fid_bhatt_ataque:.6f}")
print(f"Bhattacharyya coef.  mitigado : {fid_bhatt_mitigado:.6f}")
print(f"Hellinger distancia  ataque   : {dist_hellinger_ataque:.6f}")
print(f"Hellinger distancia  mitigado : {dist_hellinger_mitigado:.6f}")
print(f"Jensen-Shannon dist. ataque   : {dist_js_ataque:.6f}")
print(f"Jensen-Shannon dist. mitigado : {dist_js_mitigado:.6f}")
print(f"Wasserstein dist.    ataque   : {dist_wass_ataque:.6f}")
print(f"Wasserstein dist.    mitigado : {dist_wass_mitigado:.6f}")

# ==========================================
# 4. TABLA COMPARATIVA
# ==========================================
print("\n" + "=" * 60)
print("TABLA COMPARATIVA DE MÉTRICAS")
print("=" * 60)

datos_tabla = [
    ["Métrica", "Ataque (%)", "Mitigado (%)", "Recuperación (pp)"],
    ["-" * 20, "-" * 12, "-" * 14, "-" * 18],
    ["Bhattacharyya", f"{fid_bhatt_ataque * 100:6.2f}", f"{fid_bhatt_mitigado * 100:6.2f}", 
     f"{(fid_bhatt_mitigado - fid_bhatt_ataque) * 100:6.2f}"],
    ["Hellinger", f"{sim_hellinger_ataque * 100:6.2f}", f"{sim_hellinger_mitigado * 100:6.2f}", 
     f"{(sim_hellinger_mitigado - sim_hellinger_ataque) * 100:6.2f}"],
    ["Jensen-Shannon", f"{sim_js_ataque * 100:6.2f}", f"{sim_js_mitigado * 100:6.2f}", 
     f"{(sim_js_mitigado - sim_js_ataque) * 100:6.2f}"],
    ["Wasserstein", f"{sim_wass_ataque * 100:6.2f}", f"{sim_wass_mitigado * 100:6.2f}", 
     f"{(sim_wass_mitigado - sim_wass_ataque) * 100:6.2f}"],
]

for fila in datos_tabla:
    print(f"{fila[0]:<20} {fila[1]:>12} {fila[2]:>14} {fila[3]:>18}")

# ==========================================
# 5. GENERACIÓN DE GRÁFICA
# ==========================================
print("\n" + "=" * 60)
print("Generando gráfica comparativa...")
print("=" * 60)

metricas = ['Bhattacharyya', 'Hellinger', 'Jensen-Shannon', 'Wasserstein']
valores_ataque = [
    fid_bhatt_ataque * 100,
    sim_hellinger_ataque * 100,
    sim_js_ataque * 100,
    sim_wass_ataque * 100
]
valores_mitigado = [
    fid_bhatt_mitigado * 100,
    sim_hellinger_mitigado * 100,
    sim_js_mitigado * 100,
    sim_wass_mitigado * 100
]

x = np.arange(len(metricas))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, valores_ataque, width, label='Bajo Ataque (Sin Defensa)', color='#d62728')
rects2 = ax.bar(x + width/2, valores_mitigado, width, label='Con Aislamiento Espacial', color='#1f77b4')

# Etiquetas y formato
ax.set_ylabel('Similitud (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparación de Métricas de Similitud: Impacto y Mitigación de Crosstalk', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(metricas, fontsize=11)
ax.legend(fontsize=11, loc='lower right')
ax.set_ylim([0, 110])

# Añadir línea de referencia (línea base ideal)
ax.axhline(y=100, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Línea Base Ideal (100%)')
ax.legend(fontsize=11, loc='lower right')

# Añadir valores en las barras
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

autolabel(rects1)
autolabel(rects2)

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# Guardar
plt.savefig('Comparacion_Metricas.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada como 'Comparacion_Metricas.png'\n")

plt.show()

print("=" * 60)
print("Análisis completado")
print("=" * 60)
