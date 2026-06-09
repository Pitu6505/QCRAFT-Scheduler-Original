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

# 1. Load the '000' counts for each time window
archivos = ['Base/Espia/Espia1.json', 'Base/Espia/Espia2.json', 'Base/Espia/Espia3.json', 'Base/Espia/Espia4.json']
zero_counts = [extraer_zero_count(archivo) for archivo in archivos]

# Time windows (simulated in window steps, e.g. 0, 1500, 3000, 4500 dt)
ventanas = ['Window 1\n(Start)', 'Window 2\n(Middle)', 'Window 3\n(Middle-End)', 'Window 4\n(End)']

# 2. Generate the time bucketing chart
plt.figure(figsize=(10, 6))
plt.plot(ventanas, zero_counts, marker='o', linestyle='-', color='red', linewidth=2, markersize=8)

# Add titles and labels (academic format)
plt.xlabel('Time Windows (Time Buckets)', fontsize=16)
plt.ylabel('Zero Counts (State $|000\\rangle$)', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)

# Explanatory annotation on the chart
plt.annotate('High-Density CNOT Zone\n(QFT Algorithm)', 
             xy=(1, 3686), xytext=(1.5, 4000),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=16, bbox=dict(boxstyle="round", alpha=0.1))

# Guardar la gráfica para el paper y mostrarla
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Ataque_Snooping_QFT.png'), dpi=300, bbox_inches='tight')
plt.show()

# Show data in the console
print("=== SNOOPING RESULTS (ZERO COUNTS) ===")
for i, conteo in enumerate(zero_counts):
    print(f"Spy {i+1}: {conteo} counts")