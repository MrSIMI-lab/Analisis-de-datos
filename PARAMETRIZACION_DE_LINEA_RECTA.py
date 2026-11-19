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

    X = df_resultados["Tiempo_Pico_uS"].values
    Y = df_resultados["Altura_Pulso"].values

    # parametrizacion de la linea recta
    coeficientes, matriz_cov = np.polyfit(X, Y, deg=1, cov=True)

    m, b = coeficientes  
    error_m = np.sqrt(
        matriz_cov[0, 0]
    )  
    error_b = np.sqrt(
        matriz_cov[1, 1]
    )  

    print("\n==========================================")
    print("      RESULTADOS DEL AJUSTE LINEAL        ")
    print("==========================================")
    print(f"Ecuación: y = {m:.4f}x + {b:.4f}")
    print(f"Pendiente (m) = {m:.6f} ± {error_m:.6f}")
    print(f"Ordenada b   = {b:.6f} ± {error_b:.6f}")

    # PROPAGACIÓN DE ERRORES DE LA RECTA
    # Generamos puntos en X para dibujar la línea continua de ajuste
    x_ajuste = np.linspace(X.min(), X.max(), 200)
    y_ajuste = m * x_ajuste + b

    # Fórmula física de la propagación de errores para y = mx + b:
    # sigma_y^2 = (x * sigma_m)^2 + (1 * sigma_b)^2 + 2 * x * covarianza(m,b)
    error_y_propagado = np.sqrt(
        (x_ajuste * error_m) ** 2
        + (error_b) ** 2
        + 2 * x_ajuste * matriz_cov[0, 1]
    )

    # GRAFICACIÓN DEL DIAGRAMA DE DISPERSIÓN + AJUSTE
    plt.figure(figsize=(10, 6))

    # Puntos experimentales dispersos
    plt.scatter(
        X,
        Y,
        color="indigo",
        alpha=0.7,
        edgecolors="black",
        s=45,
        label="Datos Experimentales",
    )

    # Línea central del ajuste lineal ajustado
    plt.plot(
        x_ajuste,
        y_ajuste,
        color="crimson",
        linewidth=2,
        label=f"Ajuste Lineal: y = {m:.3f}x + {b:.3f}",
    )

    # Banda sombreada de la propagación de errores (Intervalo de confianza estándar)
    plt.fill_between(
        x_ajuste,
        y_ajuste - error_y_propagado,
        y_ajuste + error_y_propagado,
        color="crimson",
        alpha=0.15,
        label="Banda de Error Propagado (±1σ)",
    )



    # Configuración estética
    plt.title("Ajuste Lineal y Propagación de Errores en los Pulsos", fontsize=14)
    plt.xlabel("Tiempo de ocurrencia del Pico (µs)", fontsize=12)
    plt.ylabel("Altura Total del Pulso (Voltaje V)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()
