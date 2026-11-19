from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

carpeta_csv = Path("/home/mrsimi/Descargas/test_paleta2_Manuel")

alturas = []
tiempos_de_pico = []

# --- 1. PROCESAMIENTO DE ARCHIVOS ---
for archivo in carpeta_csv.glob("*.csv"):
    try:
        df = pd.read_csv(archivo, skiprows=14, header=None)

        if df.shape[1] < 2:
            continue

        df.columns = ["TIME", "VOLTAJE"]
        df["TIME"] = pd.to_numeric(df["TIME"], errors="coerce")
        df["VOLTAJE"] = pd.to_numeric(df["VOLTAJE"], errors="coerce")
        df = df.dropna(subset=["TIME", "VOLTAJE"])

        if df.empty:
            continue

        v_max = df["VOLTAJE"].max()
        v_min = df["VOLTAJE"].min()
        altura_pulso = v_max - v_min

        fila_pico = df["VOLTAJE"].idxmax()
        tiempo_pico_us = df.loc[fila_pico, "TIME"] * 1e6

        alturas.append(altura_pulso)
        tiempos_de_pico.append(tiempo_pico_us)

    except Exception as e:
        print(f"Error procesando {archivo.name}: {e}")

if len(alturas) == 0:
    print("[!] No se pudieron extraer datos válidos.")
else:
    df_resultados = pd.DataFrame(
        {"Tiempo_Pico_uS": tiempos_de_pico, "Altura_Pulso": alturas}
    )
    df_resultados = df_resultados[np.isfinite(df_resultados["Altura_Pulso"])]
    df_resultados = df_resultados[np.isfinite(df_resultados["Tiempo_Pico_uS"])]

    plt.figure(figsize=(10, 6))


    sns.histplot(
        data=df_resultados,
        x="Tiempo_Pico_uS",
        y="Altura_Pulso",
        bins=25, 
        cbar=True,  
        cmap="viridis",  
        cbar_kws={"label": "Cantidad de Pulsos (Frecuencia)"},
    )

    # Personalización estética
    plt.title(
        "Histograma Bivariado",
        fontsize=13,
    )
    plt.xlabel("Tiempo de ocurrencia del Pico (µs)", fontsize=11)
    plt.ylabel("Altura Total del Pulso (Voltaje V)", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.4)

    plt.tight_layout()
    plt.show()
