import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


def construir_matriz_mejoras():
    """Devuelve la matriz de mejoras porcentuales en Hellinger."""
    perfiles_agresores = ["Profile 1", "Profile 2", "Profile 3"]
    mitigaciones = ["Temporary isolation", "DD", "Spatial isolation"]

    mejoras = {
        "Temporary isolation": [10.45308255, -15.72510402, 5.687639145],
        "DD": [15.6249166, 54.22407463, 47.90030684],
        "Spatial isolation": [17.64508089, -102.5885774, np.nan],
    }

    matriz = np.array([mejoras[mitigacion] for mitigacion in mitigaciones], dtype=float)
    return perfiles_agresores, mitigaciones, matriz


def dibujar_heatmap(perfiles_agresores, mitigaciones, matriz):
    """Genera y guarda el mapa de calor con mejora porcentual."""
    fig, ax = plt.subplots(figsize=(11, 6))

    valores_validos = matriz[~np.isnan(matriz)]
    limite = float(np.max(np.abs(valores_validos))) if valores_validos.size else 1.0
    norm = TwoSlopeNorm(vmin=-limite, vcenter=0, vmax=limite)

    cmap = plt.get_cmap("RdYlGn")
    im = ax.imshow(matriz, cmap=cmap, norm=norm)

    ax.set_xticks(np.arange(len(perfiles_agresores)))
    ax.set_yticks(np.arange(len(mitigaciones)))
    ax.set_xticklabels(perfiles_agresores, fontsize=15)
    ax.set_yticklabels(mitigaciones, fontsize=14)
    ax.set_xlabel("Mitigation techniques", fontsize=20, fontweight="bold")
    ax.set_ylabel("Offenders Profiles", fontsize=20, fontweight="bold")

    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            valor = matriz[i, j]
            if np.isnan(valor):
                texto = "N/D"
                color_texto = "black"
            else:
                texto = f"{valor:+.2f}%".replace(".", ",")
                color_texto = "white" if abs(valor) > limite * 0.45 else "black"
            ax.text(j, i, texto, ha="center", va="center", fontsize=11, fontweight="bold", color=color_texto)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Hellinger's percentage improvement", rotation=270, labelpad=18)

    plt.tight_layout()
    salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MapaCalor_Mejora_Hellinger.png")
    plt.savefig(salida, dpi=300, bbox_inches="tight")
    plt.close()
    return salida


def main():
    perfiles_agresores, mitigaciones, matriz = construir_matriz_mejoras()

    print("=" * 70)
    print("MAPA DE CALOR DE MEJORA PORCENTUAL EN HELLINGER")
    print("=" * 70)
    print("Perfiles agresores:", ", ".join(perfiles_agresores))
    print("Mitigaciones:", ", ".join(mitigaciones))
    print("\nMatriz usada:")
    print(matriz)

    salida = dibujar_heatmap(perfiles_agresores, mitigaciones, matriz)
    print(f"\n✓ Guardado: {os.path.basename(salida)}")


if __name__ == "__main__":
    main()