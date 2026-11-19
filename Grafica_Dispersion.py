from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

carpeta_csv = Path("/home/mrsimi/Descargas/test_paleta2_Manuel")

alturas = []
tiempos_de_pico = []  

for archivo in carpeta_csv.glob("*.csv"):
    try:
       
        
        df = pd.read_csv(archivo, skiprows=14, header=None)

        if df.shape[1] < 2:
            continue

   #nombres de las columnas del csv
        df.columns = ["TIME", "CH1"]

        df["TIME"] = pd.to_numeric(df["TIME"], errors="coerce")
        df["CH1"] = pd.to_numeric(df["CH1"], errors="coerce")

        # eliminar filas vacias
        df = df.dropna(subset=["TIME", "CH1"])

        if df.empty:
            continue

        v_max = df["CH1"].max()
        v_min = df["CH1"].min()
        altura_pulso = v_max - v_min

        # ENCONTRAR EL TIEMPO EN EL QUE OCURRE EL V_MAX
        fila_pico = df["CH1"].idxmax()
       
        tiempo_pico_us = df.loc[fila_pico, "TIME"] * 1e6

        alturas.append(altura_pulso)
        tiempos_de_pico.append(tiempo_pico_us)

    except Exception as e:
        print(f"Error procesando {archivo.name}: {e}")

if len(alturas) == 0:
    print(
        "\n[!] Error: No se extrajeron datos. Verifica si las rutas o archivos contienen datos numéricos."
    )
else:
    df_resultados = pd.DataFrame(
        {"Tiempo_Pico_uS": tiempos_de_pico, "Altura_Pulso": alturas}
    )
#diagrama de dispersion
    plt.figure(figsize=(10, 6))

    plt.scatter(
        df_resultados["Tiempo_Pico_uS"],
        df_resultados["Altura_Pulso"],
        color="indigo",
        alpha=0.7,
        edgecolors="black",
        s=45,
        label="Pulso Detectado",
    )

    plt.title(
        "Posición Temporal del Pico Máximo vs Altura del Pulso", fontsize=14
    )
    plt.xlabel("Tiempo de ocurrencia del Pico (µs)", fontsize=12)
    plt.ylabel("Altura Total del Pulso (V_max - V_min)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
#clasificacion por rangos
    df_resultados = df_resultados[np.isfinite(df_resultados["Altura_Pulso"])]
    
    df_resultados["Rango_Voltaje"] = pd.cut(
        df_resultados["Altura_Pulso"], bins=30
    )
    clasificacion_rangos = (
        df_resultados["Rango_Voltaje"].value_counts().sort_index().reset_index()
    )
    clasificacion_rangos.columns = [
        "Rango de Altura (V)",
        "Cantidad de Pulsos",
    ]
    print("\n--- Clasificación por rangos de voltaje ---")
    print(clasificacion_rangos.to_string(index=False))
