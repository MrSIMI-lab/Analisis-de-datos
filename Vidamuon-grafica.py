from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

carpeta_csv = Path("/home/mrsimi/Descargas/calibration_TAC/test_2micro")
alturas = []

for archivo in carpeta_csv.glob("*.csv"):
    try:
        df = pd.read_csv(archivo, skiprows=13)
        columna_voltaje = df.columns[1]
        valores_numericos = pd.to_numeric(df[columna_voltaje], errors="coerce")

        v_max = valores_numericos.max()
        v_min = valores_numericos.min()
        altura_pulso = v_max - v_min

        alturas.append(altura_pulso)

    except Exception as e:
        print(f"Error procesando {archivo.name}: {e}")

df_resultados = pd.DataFrame(alturas, columns=["Altura_Pulso"])
df_limpio = df_resultados[np.isfinite(df_resultados["Altura_Pulso"])]

#Configuración y diseño del Histograma
plt.figure(figsize=(10, 6))

# plt.hist calcula los rangos y dibuja las barras automáticamente
plt.hist(
    df_limpio["Altura_Pulso"],
    bins=30,
    color="skyblue",
    edgecolor="black",
    alpha=0.8,
)

#Etiquetas y títulos
plt.title(
    "Distribución de Alturas de Pulso (Vida Media del Muón)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Altura del Pulso (V)", fontsize=12)
plt.ylabel("Cantidad de Pulsos / Archivos", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)

#Muestra la gráfica en pantalla
plt.tight_layout()
plt.show()
