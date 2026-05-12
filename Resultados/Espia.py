import json
import matplotlib.pyplot as plt
import os

def extraer_zero_count(ruta_archivo):
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_script, ruta_archivo)

    with open(ruta_completa, 'r') as f:
        datos = json.load(f)

        if not isinstance(datos, list):
            raise ValueError(f"Formato JSON invalido en {ruta_archivo}: se esperaba una lista")

        for entrada in datos:
            circuito = str(entrada.get('circuit', '')).lower()
            identificador = str(entrada.get('_id', '')).lower()
            if '/espia/' in circuito or identificador.startswith('circuito_espia'):
                return entrada.get('value', {}).get('000', 0)

        raise ValueError(
            f"No se encontro la ejecucion del espia en {ruta_archivo}. "
            "Asegura que el JSON contenga un documento de circuito_espia_X.py."
        )

# 1. Cargar los conteos '000' de cada ventana temporal
archivos = ['Espia/Espia1.json', 'Espia/Espia2.json', 'Espia/Espia3.json', 'Espia/Espia4.json']
zero_counts = [extraer_zero_count(archivo) for archivo in archivos]

# Las ventanas de tiempo (simuladas en pasos de la ventana, ej. 0, 1500, 3000, 4500 dt)
ventanas = ['Ventana 1\n(Inicio)', 'Ventana 2\n(Medio)', 'Ventana 3\n(Medio-Fin)', 'Ventana 4\n(Fin)']

# 2. Generar el gráfico de Time Bucketing
plt.figure(figsize=(10, 6))
plt.plot(ventanas, zero_counts, marker='o', linestyle='-', color='red', linewidth=2, markersize=8)

# Añadir títulos y etiquetas (Formato académico)
plt.title('Ataque de Canal Lateral (Snooping): Extracción de la Actividad de la Víctima', fontsize=14)
plt.xlabel('Ventanas de Tiempo (Time Buckets)', fontsize=12)
plt.ylabel('Zero Counts (Estado $|000\\rangle$)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Anotaciones explicativas en el gráfico
plt.annotate('Zona de Alta Densidad\nde CNOTs (Algoritmo QFT)', 
             xy=(1, 3686), xytext=(1.5, 4000),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10, bbox=dict(boxstyle="round", alpha=0.1))

# Guardar la gráfica para el paper y mostrarla
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Ataque_Snooping_QFT.png'), dpi=300, bbox_inches='tight')
plt.show()

# Mostrar datos por consola
print("=== RESULTADOS DEL SNOOPING (ZERO COUNTS) ===")
for i, conteo in enumerate(zero_counts):
    print(f"Espía {i+1} : {conteo} conteos")