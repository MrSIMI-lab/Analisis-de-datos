import numpy as np
import pandas as pd

# 1. Cargar el archivo CSV del osciloscopio
# Nota: Si tu archivo tiene filas de encabezado con metadatos del osciloscopio, 
# puedes saltarlas usando el parámetro: skiprows=X (ej. skiprows=10)
df = pd.read_csv('/home/mrsimi/Descargas/test_muon_lifetime_1/SaveOnEvent_ch1_20260521151734573.csv')

# 2. Identificar correctamente los nombres de tus columnas
# Reemplaza 'Tiempo' y 'Voltaje' por los nombres exactos que vengan en tu CSV
col_tiempo = 'TIME'    # Eje X
col_voltaje = 'CH1'  # Eje Y

# 3. Encontrar las filas donde ocurren el máximo y el mínimo de voltaje
fila_max = df.loc[df[col_voltaje].idxmax()]
fila_min = df.loc[df[col_voltaje].idxmin()]

# 4. Extraer las coordenadas (X, Y) de ambos puntos
t_max, v_max = fila_max[col_tiempo], fila_max[col_voltaje]
t_min, v_min = fila_min[col_tiempo], fila_min[col_voltaje]

# 5. Calcular las distancias individuales (Diferencias)
delta_v = abs(v_max - v_min)  # Distancia vertical (Voltaje Pico a Pico)
delta_t = abs(t_max - t_min)  # Distancia horizontal (Intervalo de tiempo)

# 6. Calcular la distancia geométrica directa (Euclidiana) si fuera necesario
distancia_euclidiana = np.sqrt((t_max - t_min)**2 + (v_max - v_min)**2)

# 7. Mostrar los resultados en la terminal de Linux
print(f"Punto Máximo: Tiempo = {t_max} s, Voltaje = {v_max} V")
print(f"Punto Mínimo: Tiempo = {t_min} s, Voltaje = {v_min} V")
print("-" * 50)
print(f"Distancia en Voltaje (ΔV): {delta_v} V")
print(f"Distancia en Tiempo (Δt): {delta_t} s")
print(f"Distancia Euclidiana directa: {distancia_euclidiana}")
