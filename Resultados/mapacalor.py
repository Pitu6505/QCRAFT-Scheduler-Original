import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import wasserstein_distance

# ==========================================
# FUNCIONES DE CARGA DE DATOS
# ==========================================

def cargar_conteos(ruta_archivo):
    """
    Carga los conteos de un archivo JSON.
    Si hay múltiples resultados, busca específicamente el de la víctima.
    """
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_script, ruta_archivo)
    
    with open(ruta_completa, 'r') as f:
        datos = json.load(f)

        # Si es un único resultado
        if isinstance(datos, list) and len(datos) == 1:
            return datos[0]['value']

        # Si hay múltiples resultados, busca la víctima
        for entrada in datos:
            circuito = str(entrada.get('circuit', '')).lower()
            identificador = str(entrada.get('_id', '')).lower()
            
            if 'qft' in identificador or 'victima' in circuito:
                return entrada['value']

        # Si no encuentra la víctima, retorna el primer valor
        return datos[0]['value']


# ==========================================
# FUNCIONES DE DISTANCIA
# ==========================================

def normalizar_distribucion(counts, total_shots=10000):
    """Convierte conteos a probabilidades normalizadas."""
    return {estado: conteo / total_shots for estado, conteo in counts.items()}


def distancia_hellinger(dist_p, dist_q):
    """
    Calcula la distancia de Hellinger entre dos distribuciones.
    Rango: [0, 1] (0 = idénticas, 1 = completamente diferentes)
    """
    estados_posibles = set(list(dist_p.keys()) + list(dist_q.keys()))
    suma = 0.0
    
    for estado in estados_posibles:
        p = dist_p.get(estado, 0)
        q = dist_q.get(estado, 0)
        suma += (math.sqrt(p) - math.sqrt(q)) ** 2
    
    return math.sqrt(suma / 2)


def divergencia_jensen_shannon(dist_p, dist_q):
    """
    Calcula la divergencia Jensen-Shannon entre dos distribuciones.
    Métrica simétrica de la divergencia KL.
    Rango: [0, 1]
    """
    estados_posibles = set(list(dist_p.keys()) + list(dist_q.keys()))
    
    # Crear vectores de probabilidad
    p_vals = np.array([dist_p.get(estado, 0) for estado in sorted(estados_posibles)])
    q_vals = np.array([dist_q.get(estado, 0) for estado in sorted(estados_posibles)])
    
    # Normalizar por si acaso
    p_vals = p_vals / p_vals.sum()
    q_vals = q_vals / q_vals.sum()
    
    # JS divergence = sqrt(KL(p || m) + KL(q || m)) / sqrt(2), donde m = (p+q)/2
    m = (p_vals + q_vals) / 2
    
    # Evitar log(0)
    p_vals = np.where(p_vals > 1e-10, p_vals, 1e-10)
    q_vals = np.where(q_vals > 1e-10, q_vals, 1e-10)
    m = np.where(m > 1e-10, m, 1e-10)
    
    kl_pm = np.sum(p_vals * np.log(p_vals / m))
    kl_qm = np.sum(q_vals * np.log(q_vals / m))
    
    js_div = (kl_pm + kl_qm) / 2
    return math.sqrt(max(js_div, 0))  # JS distance es la raíz


def distancia_wasserstein(counts_p, counts_q, total_shots=10000):
    """
    Calcula la distancia de Wasserstein entre dos distribuciones discretas.
    Interpreta los estados binarios como números y calcula el costo de transportar
    la masa de probabilidad.
    """
    estados = sorted(set(list(counts_p.keys()) + list(counts_q.keys())))
    
    # Convertir estados binarios a números decimales para el cálculo
    # e.g., "00000" -> 0, "00001" -> 1, etc.
    indices = [int(estado, 2) for estado in estados]
    
    # Obtener probabilidades
    p_vals = np.array([counts_p.get(estado, 0) / total_shots for estado in estados])
    q_vals = np.array([counts_q.get(estado, 0) / total_shots for estado in estados])
    
    # Normalizar
    p_vals = p_vals / p_vals.sum()
    q_vals = q_vals / q_vals.sum()
    
    # Calcular distancia de Wasserstein 1D
    w_dist = wasserstein_distance(indices, indices, p_vals, q_vals)
    
    # Normalizar por el rango máximo (32 - 0 = 31 para 5 qubits)
    w_dist_normalizado = w_dist / 31
    
    return w_dist, w_dist_normalizado


def fidelidad_bhattacharyya(dist_p, dist_q):
    """Calcula el coeficiente de similitud de Bhattacharyya."""
    estados_posibles = set(list(dist_p.keys()) + list(dist_q.keys()))
    fidelidad = 0.0
    
    for estado in estados_posibles:
        p = dist_p.get(estado, 0)
        q = dist_q.get(estado, 0)
        fidelidad += math.sqrt(p * q)
    
    return fidelidad


# ==========================================
# CARGA DE DATOS
# ==========================================

print("=" * 70)
print("ANÁLISIS COMPLETO DE DISTANCIAS Y COMPARACIÓN DE CIRCUITOS")
print("=" * 70)
print("\nCargando datos...")

# Cargar conteos (sin normalizar aún)
counts_base = cargar_conteos('Victima/qft.json')
counts_atacado = cargar_conteos('Base/Perfil2/PerfilAlto2.json')
counts_mitigado = cargar_conteos('DesacoplamientoDinamico/Perfil2/PerfilAlto2Desa.json')

# Normalizar a distribuciones de probabilidad
dist_base = normalizar_distribucion(counts_base)
dist_atacado = normalizar_distribucion(counts_atacado)
dist_mitigado = normalizar_distribucion(counts_mitigado)

print("✓ Datos cargados exitosamente\n")

# ==========================================
# CÁLCULO DE DISTANCIA DE HELLINGER
# ==========================================

print("=" * 70)
print("CÁLCULO DE DISTANCIA DE HELLINGER")
print("=" * 70)

hellinger_base_ataque = distancia_hellinger(dist_base, dist_atacado)
hellinger_base_mitig = distancia_hellinger(dist_base, dist_mitigado)
hellinger_ataque_mitig = distancia_hellinger(dist_atacado, dist_mitigado)

print(f"\nBase vs Atacado   : {hellinger_base_ataque:.6f}".replace('.', ','))
print(f"Base vs Mitigado  : {hellinger_base_mitig:.6f}".replace('.', ','))
print(f"Atacado vs Mitigado: {hellinger_ataque_mitig:.6f}".replace('.', ','))

# ==========================================
# GENERACIÓN DE MAPA DE CALOR
# ==========================================

print("\n" + "=" * 70)
print("GENERACIÓN DE MAPA DE CALOR")
print("=" * 70)

matriz_hellinger = np.array([
    [0.0, hellinger_base_ataque, hellinger_base_mitig],
    [hellinger_base_ataque, 0.0, hellinger_ataque_mitig],
    [hellinger_base_mitig, hellinger_ataque_mitig, 0.0],
])

etiquetas = ['Base', 'Atacado', 'Mitigado']

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(matriz_hellinger, cmap='viridis', vmin=0, vmax=1)

ax.set_xticks(np.arange(len(etiquetas)))
ax.set_yticks(np.arange(len(etiquetas)))
ax.set_xticklabels(etiquetas, fontsize=11)
ax.set_yticklabels(etiquetas, fontsize=11)
ax.set_title('Mapa de calor de distancia de Hellinger', fontsize=14, fontweight='bold')

for i in range(len(etiquetas)):
    for j in range(len(etiquetas)):
        valor = matriz_hellinger[i, j]
        color_texto = 'white' if valor > 0.5 else 'black'
        ax.text(j, i, f'{valor:.3f}'.replace('.', ','), ha='center', va='center', color=color_texto, fontsize=11)

cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Distancia de Hellinger', rotation=270, labelpad=15)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'MapaCalor_Hellinger.png'), dpi=300, bbox_inches='tight')
print("✓ Guardado: MapaCalor_Hellinger.png")
plt.close()

print("\n" + "=" * 70)
print("ANÁLISIS COMPLETADO EXITOSAMENTE")
print("=" * 70)
print("\nArchivo generado:")
print("  • MapaCalor_Hellinger.png - Mapa de calor de distancias Hellinger")
print()
