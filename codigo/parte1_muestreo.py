# =============================================================================
# Estudio Estadístico de la Demanda Turística Emisiva Uruguaya
# Probabilidad y Estadística Aplicada — Facultad de Ingeniería y Tecnologías
#
# PARTE 1: Adquisición de datos y muestreo aleatorio equiprobable
#
# Descripción:
#   Este script carga el archivo CSV de Turismo Emisivo publicado por el
#   Ministerio de Turismo del Uruguay en el catálogo de datos abiertos
#   (catalogodatos.gub.uy), selecciona de forma aleatoria y equiprobable
#   2,000 filas del total de 32,109 registros disponibles, y exporta esa
#   muestra a un nuevo archivo CSV que será la base de todo el análisis
#   posterior (Partes 2 y 3).
#
#   Contexto de investigación:
#   El turismo emisivo refiere a los viajes realizados por residentes
#   uruguayos hacia el exterior. El dataset contiene información sobre
#   destino, fechas, gastos desagregados, medios de transporte y perfil
#   sociodemográfico del viajero. Se trabaja con una muestra probabilística
#   para garantizar representatividad estadística.
#
# Requisitos:
#   Instalar dependencias desde la raíz del proyecto:
#     pip install -r requirements.txt
#
# Uso:
#   Colocar el archivo "emisivo.csv" en la carpeta datos/ y ejecutar
#   desde la raíz del proyecto:
#     python codigo/parte1_muestreo.py
# =============================================================================

# --- Importación de librerías ------------------------------------------------
import pandas as pd  # Librería para manipulación de datos tabulares

# --- Parámetros configurables ------------------------------------------------

RUTA_ARCHIVO_ORIGINAL = "datos/emisivo.csv"  # Nombre del archivo fuente descargado
RUTA_ARCHIVO_MUESTRA = "datos/muestra_2000.csv"  # Nombre del archivo de salida
TAMANIO_MUESTRA = 2000  # Cantidad de filas a seleccionar
SEMILLA_ALEATORIA = 42  # Semilla fija para reproducibilidad:
# garantiza que cualquier persona que
# ejecute este script obtenga
# exactamente las mismas 2000 filas.

# --- Paso 1: Cargar el archivo CSV completo ----------------------------------
# pd.read_csv() lee el archivo y lo convierte en un DataFrame (tabla de datos).
# Un DataFrame es la estructura de datos principal de pandas: filas y columnas,
# similar a una hoja de cálculo.

print("=" * 60)
print("PARTE 1 - Muestreo aleatorio del dataset de Turismo Emisivo")
print("=" * 60)

print(f"\n[1/4] Cargando el archivo '{RUTA_ARCHIVO_ORIGINAL}'...")
df_completo = pd.read_csv(RUTA_ARCHIVO_ORIGINAL)

# Mostrar dimensiones del dataset completo
n_filas, n_columnas = df_completo.shape
print(f"      Dataset cargado correctamente.")
print(f"      Total de filas    : {n_filas:,}")
print(f"      Total de columnas : {n_columnas}")

# --- Paso 2: Muestreo aleatorio equiprobable ---------------------------------
# .sample() selecciona filas al azar del DataFrame.
#
#   n          : cantidad de filas a seleccionar (2000 en este caso).
#   replace    : False → muestreo SIN reposición, es decir, cada fila
#                puede aparecer como máximo una vez en la muestra.
#   random_state: semilla aleatoria para reproducibilidad.
#
# El muestreo es EQUIPROBABLE: cada posible muestra de tamaño 2.000 tiene
# exactamente la misma probabilidad de ser la seleccionada.
# La probabilidad de que una muestra específica sea elegida es:
#
#   P(selección) = 1 / C(32.109, 2.000)
#
# donde C(N, n) = N! / (n! · (N-n)!) es el número de combinaciones posibles
# de N elementos tomados de a n. No es 2000/32109, que corresponde a la
# probabilidad de inclusión marginal de un elemento individual.

print(
    f"\n[2/4] Seleccionando {TAMANIO_MUESTRA} filas al azar (semilla={SEMILLA_ALEATORIA})..."
)
df_muestra = df_completo.sample(
    n=TAMANIO_MUESTRA, replace=False, random_state=SEMILLA_ALEATORIA
)

# Reordenar los índices para que la muestra quede numerada desde 0
df_muestra = df_muestra.reset_index(drop=True)

print(f"      Muestreo completado.")
print(f"      Filas seleccionadas: {len(df_muestra):,}")

# --- Paso 3: Exportar la muestra a un nuevo archivo CSV ----------------------
# .to_csv() guarda el DataFrame en disco como archivo CSV.
#   index=False → no incluye la columna de índices en el archivo exportado.

print(f"\n[3/4] Exportando la muestra al archivo '{RUTA_ARCHIVO_MUESTRA}'...")
df_muestra.to_csv(RUTA_ARCHIVO_MUESTRA, index=False)
print(f"      Archivo exportado correctamente.")

# --- Paso 4: Resumen de verificación ----------------------------------------
# Se muestra un resumen para verificar que todo salió bien antes de continuar
# con el análisis.

print(f"\n[4/4] Resumen de verificación:")
print(f"      Columnas del dataset : {list(df_muestra.columns)}")
print(f"\n      Primeras 3 filas de la muestra:")
print(df_muestra.head(3).to_string())
print(f"\n      Tipos de datos por columna:")
print(df_muestra.dtypes.to_string())
print(f"\n      Valores faltantes por columna:")
print(df_muestra.isnull().sum().to_string())

print("\n" + "=" * 60)
print(f"Proceso finalizado. El archivo '{RUTA_ARCHIVO_MUESTRA}' está")
print("listo para ser utilizado en las Partes 2 y 3 del análisis.")
print("=" * 60)
