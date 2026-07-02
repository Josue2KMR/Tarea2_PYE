# =============================================================================
# Estudio Estadístico de la Demanda Turística Emisiva Uruguaya
# Probabilidad y Estadística Aplicada — Facultad de Ingeniería y Tecnologías
#
# PARTE 2: Estadística Descriptiva
#
# Descripción:
#   Este script realiza el análisis descriptivo completo sobre la muestra de
#   2,000 observaciones generada en la Parte 1. Incluye clasificación de
#   variables, tablas de frecuencias (absolutas, relativas y por intervalos),
#   gráficos de distribución y medidas de posición y dispersión.
#
#   Contexto de investigación:
#   Antes de realizar inferencias sobre la población de turistas uruguayos,
#   es necesario comprender la estructura de los datos disponibles. La
#   estadística descriptiva permite identificar patrones en los destinos
#   elegidos, la distribución del gasto en alojamiento y la relación entre
#   el tamaño del grupo y el gasto total.
#
#   Variable de gasto seleccionada: GastoAlojamiento
#   Justificación: permite coherencia con el test de hipótesis de la Parte 3
#   (ítem 3.2), donde se evalúa si el gasto medio en alojamiento es < $350.
#
# Requisitos:
#   Instalar dependencias desde la raíz del proyecto:
#     pip install -r requirements.txt
#
# Uso:
#   Desde la raíz del proyecto ejecutar:
#     python codigo/parte2_descriptiva.py
#   Los gráficos se guardan automáticamente en la carpeta resultados/
# =============================================================================

# --- Importación de librerías ------------------------------------------------
import pandas as pd          # Manipulación de datos tabulares
import numpy as np           # Operaciones numéricas y matemáticas
import matplotlib.pyplot as plt  # Generación de gráficos
import matplotlib.ticker as mticker
import os                    # Manejo de rutas y carpetas

# --- Configuración general ---------------------------------------------------

RUTA_MUESTRA    = os.path.join("datos", "muestra_2000.csv")
RUTA_RESULTADOS = "resultados"   # Carpeta donde se guardan los gráficos
VAR_GASTO       = "GastoAlojamiento"  # Variable de gasto seleccionada

# Crear carpeta de resultados si no existe
os.makedirs(RUTA_RESULTADOS, exist_ok=True)

# Estilo visual uniforme para todos los gráficos
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

print("=" * 65)
print("PARTE 2 - Estadística Descriptiva — Turismo Emisivo Uruguay")
print("=" * 65)

# --- Carga de datos ----------------------------------------------------------
print("\n[Carga] Leyendo muestra_2000.csv...")
df = pd.read_csv(RUTA_MUESTRA)
print(f"        Filas: {len(df):,}  |  Columnas: {df.shape[1]}")


# =============================================================================
# ÍTEM 2.2 — Tabla de frecuencias para la variable Destino
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 2.2 — Tabla de frecuencias: Destino")
print("─" * 65)

# Contamos cuántas veces aparece cada categoría de Destino.
# value_counts() devuelve los conteos en orden descendente.
frec_abs = df["Destino"].value_counts()           # Frecuencia absoluta (fi)
total    = frec_abs.sum()                          # Total de observaciones (n)
frec_rel = (frec_abs / total * 100).round(2)       # Frecuencia relativa en %

# Construimos la tabla final uniendo ambas series en un DataFrame
tabla_destino = pd.DataFrame({
    "Destino"              : frec_abs.index,
    "Frec. Absoluta (fi)"  : frec_abs.values,
    "Frec. Relativa (%)"   : frec_rel.values,
})

# Añadimos fila de totales
total_row = pd.DataFrame([{
    "Destino"             : "TOTAL",
    "Frec. Absoluta (fi)" : total,
    "Frec. Relativa (%)"  : 100.00,
}])
tabla_destino = pd.concat([tabla_destino, total_row], ignore_index=True)

print("\nTabla de frecuencias — Variable: Destino")
print(tabla_destino.to_string(index=False))


# =============================================================================
# ÍTEM 2.3 — Gráfico de barras y gráfico circular para Destino
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 2.3 — Gráficos: Destino")
print("─" * 65)

# Usamos los datos sin la fila TOTAL para graficar
datos_graf = tabla_destino[tabla_destino["Destino"] != "TOTAL"].copy()
datos_graf = datos_graf.sort_values("Frec. Absoluta (fi)", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(
    "Distribución de viajes por Destino\n(Muestra n = 2,000 — Turismo Emisivo Uruguay)",
    fontsize=13, fontweight="bold", y=1.01
)

# ---- Gráfico de barras ----
colores = plt.cm.tab10.colors
axes[0].bar(
    datos_graf["Destino"],
    datos_graf["Frec. Absoluta (fi)"],
    color=colores[:len(datos_graf)],
    edgecolor="white",
    width=0.7
)
axes[0].set_title("Gráfico de Barras", fontweight="bold")
axes[0].set_xlabel("Destino")
axes[0].set_ylabel("Frecuencia Absoluta")
axes[0].tick_params(axis="x", rotation=45)
# Etiquetas de valor sobre cada barra
for bar in axes[0].patches:
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 10,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=9
    )
axes[0].set_ylim(0, datos_graf["Frec. Absoluta (fi)"].max() * 1.15)

# ---- Gráfico circular (pie chart) ----
# Agrupamos categorías con < 1% en "Otros" para mejorar la legibilidad
umbral   = 1.0   # porcentaje mínimo para aparecer por separado
mayores  = datos_graf[datos_graf["Frec. Relativa (%)"] >= umbral]
menores  = datos_graf[datos_graf["Frec. Relativa (%)"] <  umbral]

if not menores.empty:
    otros_fila = pd.DataFrame([{
        "Destino"              : "Otros",
        "Frec. Absoluta (fi)"  : menores["Frec. Absoluta (fi)"].sum(),
        "Frec. Relativa (%)"   : menores["Frec. Relativa (%)"].sum(),
    }])
    pie_data = pd.concat([mayores, otros_fila], ignore_index=True)
else:
    pie_data = mayores.copy()

wedges, texts, autotexts = axes[1].pie(
    pie_data["Frec. Relativa (%)"],
    labels=pie_data["Destino"],
    autopct="%1.1f%%",
    startangle=140,
    colors=colores[:len(pie_data)],
    pctdistance=0.75
)
for t in autotexts:
    t.set_fontsize(8)
axes[1].set_title("Gráfico Circular", fontweight="bold")

plt.tight_layout()
ruta_graf_destino = os.path.join(RUTA_RESULTADOS, "grafico_destino.png")
plt.savefig(ruta_graf_destino, bbox_inches="tight")
plt.close()
print(f"  Gráfico guardado: {ruta_graf_destino}")


# =============================================================================
# ÍTEM 2.4 — Tabla de frecuencias por intervalos: GastoAlojamiento
# =============================================================================
print("\n" + "─" * 65)
print(f"ÍTEM 2.4 — Tabla de frecuencias por intervalos: {VAR_GASTO}")
print("─" * 65)

serie_gasto = df[VAR_GASTO]

# Determinamos el número de intervalos usando la regla de Sturges:
# k = 1 + log2(n), donde n es el tamaño de la muestra.
# Esta regla es ampliamente utilizada en estadística descriptiva.
n_obs = len(serie_gasto)
k     = int(np.ceil(1 + np.log2(n_obs)))   # Número de clases/intervalos

# Calculamos el ancho de cada intervalo y lo redondeamos a un número limpio
rango       = serie_gasto.max() - serie_gasto.min()
ancho_exacto = rango / k
ancho        = np.ceil(ancho_exacto / 100) * 100   # Redondeo al 100 superior

# Definimos los límites de los intervalos
lim_inf = serie_gasto.min()          # Límite inferior del primer intervalo
lim_sup = lim_inf + k * ancho        # Límite superior del último intervalo
bins    = np.arange(lim_inf, lim_sup + ancho, ancho)

# pd.cut() asigna cada observación al intervalo correspondiente.
# right=False → los intervalos son del tipo [a, b), cerrado a la izquierda.
categorias = pd.cut(serie_gasto, bins=bins, right=False, include_lowest=True)

# Calculamos frecuencias
fi    = categorias.value_counts(sort=False)   # Frecuencias absolutas
n     = fi.sum()                              # Total
fri   = (fi / n).round(6)                    # Frecuencias relativas
Fri   = fri.cumsum().round(6)                 # Frecuencias relativas acumuladas
marca = [(iv.left + iv.right) / 2 for iv in fi.index]  # Marca de clase

tabla_gasto = pd.DataFrame({
    "Intervalo"                   : [str(iv) for iv in fi.index],
    "Marca de clase"              : [round(m, 2) for m in marca],
    "Frec. Absoluta (fi)"         : fi.values,
    "Frec. Relativa (fri)"        : fri.values.round(4),
    "Frec. Rel. Acumulada (Fri)"  : Fri.values.round(4),
})

total_row2 = pd.DataFrame([{
    "Intervalo"                  : "TOTAL",
    "Marca de clase"             : "—",
    "Frec. Absoluta (fi)"        : n,
    "Frec. Relativa (fri)"       : round(fri.sum(), 4),
    "Frec. Rel. Acumulada (Fri)" : "—",
}])
tabla_gasto = pd.concat([tabla_gasto, total_row2], ignore_index=True)

print(f"\nTabla de frecuencias por intervalos — Variable: {VAR_GASTO}")
print(f"  Regla de Sturges: k = {k} intervalos | Ancho = {ancho:.0f} USD")
print()
print(tabla_gasto.to_string(index=False))


# =============================================================================
# ÍTEM 2.5 — Histograma: GastoAlojamiento
# =============================================================================
print("\n" + "─" * 65)
print(f"ÍTEM 2.5 — Histograma: {VAR_GASTO}")
print("─" * 65)

fig, ax = plt.subplots(figsize=(10, 5))

# El histograma usa los mismos bins definidos para la tabla de frecuencias,
# garantizando coherencia entre la tabla y el gráfico.
n_hist, bins_hist, patches = ax.hist(
    serie_gasto,
    bins=bins,
    edgecolor="white",
    color="#2c7bb6",
    linewidth=0.8
)

# Línea de la media y mediana para referencia visual de asimetría
media   = serie_gasto.mean()
mediana = serie_gasto.median()
ax.axvline(media,   color="#d7191c", linestyle="--", linewidth=1.5,
           label=f"Media = {media:.2f} USD")
ax.axvline(mediana, color="#1a9641", linestyle="-",  linewidth=1.5,
           label=f"Mediana = {mediana:.2f} USD")

ax.set_title(
    f"Histograma — {VAR_GASTO}\n(Muestra n = {n_obs:,} — Turismo Emisivo Uruguay)",
    fontweight="bold"
)
ax.set_xlabel("Gasto en Alojamiento (USD)")
ax.set_ylabel("Frecuencia Absoluta")
ax.legend(fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()

ruta_hist = os.path.join(RUTA_RESULTADOS, "histograma_gasto_alojamiento.png")
plt.savefig(ruta_hist, bbox_inches="tight")
plt.close()
print(f"  Gráfico guardado: {ruta_hist}")
print(f"\n  Media    = {media:.2f} USD")
print(f"  Mediana  = {mediana:.2f} USD")
print(f"  Asimetría (skewness) = {serie_gasto.skew():.4f}")
print("  → Si Media > Mediana y skewness > 0: distribución asimétrica a la derecha.")


# =============================================================================
# ÍTEM 2.6 — Diagrama de cajas: GastoAlojamiento
# =============================================================================
print("\n" + "─" * 65)
print(f"ÍTEM 2.6 — Diagrama de cajas: {VAR_GASTO}")
print("─" * 65)

# Calculamos las medidas de posición manualmente para incluirlas en el informe.
# Los cuartiles dividen la distribución en cuatro partes iguales.
Q1  = serie_gasto.quantile(0.25)   # Primer cuartil  (percentil 25)
Q2  = serie_gasto.quantile(0.50)   # Mediana          (percentil 50)
Q3  = serie_gasto.quantile(0.75)   # Tercer cuartil  (percentil 75)
IQR = Q3 - Q1                      # Rango intercuartílico

# Límites para detectar datos atípicos (outliers) usando el criterio de Tukey:
# Son atípicos los valores que caen fuera del rango [Q1 - 1.5·IQR, Q3 + 1.5·IQR]
lim_inf_out = Q1 - 1.5 * IQR
lim_sup_out = Q3 + 1.5 * IQR
outliers    = serie_gasto[(serie_gasto < lim_inf_out) | (serie_gasto > lim_sup_out)]

print(f"\n  Medidas de posición — {VAR_GASTO}:")
print(f"    Q1  (primer cuartil)   = {Q1:.2f} USD")
print(f"    Q2  (mediana)          = {Q2:.2f} USD")
print(f"    Q3  (tercer cuartil)   = {Q3:.2f} USD")
print(f"    IQR (rango intercuart) = {IQR:.2f} USD")
print(f"\n  Detección de outliers (criterio de Tukey):")
print(f"    Límite inferior = {lim_inf_out:.2f} USD")
print(f"    Límite superior = {lim_sup_out:.2f} USD")
print(f"    Datos atípicos encontrados: {len(outliers):,}")

# Nota sobre Q1 = 0:
# El primer cuartil es efectivamente $0 porque el 39.2% de la muestra
# (784 de 2.000 registros) registra GastoAlojamiento = 0. Esto ocurre en
# viajes de día (sin pernocte) o cuando los viajeros se alojan en casa de
# familiares o amigos sin costo monetario. Es un resultado correcto y
# estadísticamente válido, no un error de datos.
pct_ceros = (serie_gasto == 0).mean() * 100
print(f"\n  Nota: el {pct_ceros:.1f}% de los registros tiene GastoAlojamiento = 0.")
print(f"  Esto refleja viajes sin pernocte o alojamiento no monetario.")
print(f"  Por lo tanto Q1 = $0 es matemáticamente correcto.")

# El boxplot tiene un problema visual importante cuando Q1 = 0 y existen
# outliers de hasta $6.220: la caja queda aplastada en la base y los
# datos numéricos no se aprecian. Se resuelve con un diseño de dos paneles:
#   Panel izquierdo: vista completa (escala real) para mostrar los outliers.
#   Panel derecho: zoom a [0, lim_sup_out] para leer claramente Q1, Q2, Q3.

fig, axes = plt.subplots(1, 2, figsize=(13, 6),
                          gridspec_kw={"width_ratios": [1, 1.6]})
fig.suptitle(
    f"Diagrama de Cajas — {VAR_GASTO}\n(Muestra n = {n_obs:,} — Turismo Emisivo Uruguay)",
    fontweight="bold", fontsize=12
)

BP_STYLE = dict(
    patch_artist=True,
    widths=0.5,
    boxprops=dict(facecolor="#aec6cf", color="#2c7bb6", linewidth=1.5),
    medianprops=dict(color="#d7191c", linewidth=2.5),
    whiskerprops=dict(color="#2c7bb6", linewidth=1.5),
    capprops=dict(color="#2c7bb6", linewidth=2),
    flierprops=dict(marker="o", markerfacecolor="#fdae61",
                    markersize=3, linestyle="none", alpha=0.4),
)

# ── Panel izquierdo: escala completa ──────────────────────────────────────
ax0 = axes[0]
ax0.boxplot(serie_gasto, vert=True, **BP_STYLE)
ax0.set_title("Escala completa", fontsize=10, pad=4)
ax0.set_ylabel("Gasto en Alojamiento (USD)")
ax0.set_xticks([])
ax0.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Anotaciones en panel izquierdo
for val, lbl, dy in [
    (Q1,          f"Q1 = ${Q1:.0f} ({pct_ceros:.0f}% sin gasto)", 300),
    (Q2,          f"Q2 = ${Q2:.0f}",   200),
    (Q3,          f"Q3 = ${Q3:.0f}",   200),
    (lim_sup_out, f"Bigote = ${lim_sup_out:.0f}", 200),
]:
    ax0.annotate(lbl, xy=(1, val), xytext=(1.35, val + dy),
                 fontsize=8, color="#1a3a5c",
                 arrowprops=dict(arrowstyle="->", color="#999", lw=0.8))
ax0.annotate(f"{len(outliers)} outliers\n(> ${lim_sup_out:.0f})",
             xy=(1, serie_gasto.max()), xytext=(1.35, serie_gasto.max() - 800),
             fontsize=8, color="#b5651d",
             arrowprops=dict(arrowstyle="->", color="#999", lw=0.8))

# ── Panel derecho: zoom zona intercuartílica ──────────────────────────────
ax1 = axes[1]
ax1.boxplot(serie_gasto, vert=True, **BP_STYLE)
ax1.set_ylim(-40, lim_sup_out + 80)   # Zoom: muestra caja + bigote superior
ax1.set_title(f"Zoom zona intercuartílica [0 – ${lim_sup_out:.0f}]", fontsize=10, pad=4)
ax1.set_ylabel("Gasto en Alojamiento (USD)")
ax1.set_xticks([])
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Líneas horizontales de referencia con etiquetas
REFS = [
    (Q1,          f"Q1 = ${Q1:.2f}  ({pct_ceros:.1f}% de viajes sin gasto monetario)", "#2c7bb6"),
    (Q2,          f"Q2 (mediana) = ${Q2:.2f}",                                          "#d7191c"),
    (Q3,          f"Q3 = ${Q3:.2f}",                                                    "#2c7bb6"),
    (lim_sup_out, f"Bigote superior (Q3 + 1.5·IQR) = ${lim_sup_out:.2f}",              "#8B0000"),
]
for val, lbl, color in REFS:
    ax1.axhline(val, color=color, linestyle="--", linewidth=0.9, alpha=0.7)
    ax1.text(1.02, val, lbl, va="center", fontsize=7.5, color=color,
             transform=ax1.get_yaxis_transform())

# Flecha IQR
ax1.annotate("", xy=(0.60, Q3), xytext=(0.60, Q1),
             xycoords=("axes fraction", "data"),
             textcoords=("axes fraction", "data"),
             arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2))
ax1.text(0.57, (Q1 + Q3) / 2, f"IQR\n${IQR:.2f}",
         ha="right", va="center", fontsize=8, color="#333",
         transform=ax1.get_yaxis_transform())

plt.tight_layout()

ruta_box = os.path.join(RUTA_RESULTADOS, "boxplot_gasto_alojamiento.png")
plt.savefig(ruta_box, bbox_inches="tight")
plt.close()
print(f"\n  Gráfico guardado: {ruta_box}")


# =============================================================================
# ÍTEM 2.7 — Diagrama de dispersión: Gente vs GastoTotal
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 2.7 — Diagrama de dispersión: Gente vs GastoTotal")
print("─" * 65)

gente      = df["Gente"]
gasto_tot  = df["GastoTotal"]
correlacion = gente.corr(gasto_tot)   # Coeficiente de correlación de Pearson

# La correlación de Pearson (r) mide la fuerza y dirección de la relación
# lineal entre dos variables. Su rango es [-1, 1]:
#   r cercano a  1 → relación lineal positiva fuerte
#   r cercano a -1 → relación lineal negativa fuerte
#   r cercano a  0 → sin relación lineal aparente
print(f"\n  Coeficiente de correlación de Pearson (r) = {correlacion:.4f}")

fig, ax = plt.subplots(figsize=(9, 5))

# Usamos transparencia (alpha) para ver superposición de puntos
ax.scatter(
    gente, gasto_tot,
    alpha=0.35, s=18, color="#2c7bb6", edgecolors="none"
)

# Línea de tendencia (regresión lineal) para visualizar la relación
m, b = np.polyfit(gente, gasto_tot, 1)   # Ajuste polinomial grado 1
x_line = np.linspace(gente.min(), gente.max(), 200)
ax.plot(x_line, m * x_line + b, color="#d7191c", linewidth=2,
        label=f"Tendencia lineal (r = {correlacion:.3f})")

ax.set_title(
    "Diagrama de Dispersión — Gente vs Gasto Total\n"
    "(Muestra n = 2,000 — Turismo Emisivo Uruguay)",
    fontweight="bold"
)
ax.set_xlabel("Cantidad de personas en el grupo (Gente)")
ax.set_ylabel("Gasto Total del grupo (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(fontsize=10)
plt.tight_layout()

ruta_disp = os.path.join(RUTA_RESULTADOS, "dispersion_gente_gastototal.png")
plt.savefig(ruta_disp, bbox_inches="tight")
plt.close()
print(f"  Gráfico guardado: {ruta_disp}")


# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 65)
print("RESUMEN — Parte 2 completada")
print("=" * 65)
print(f"  Gráficos generados en: {RUTA_RESULTADOS}/")
print(f"    ├── grafico_destino.png")
print(f"    ├── histograma_gasto_alojamiento.png")
print(f"    ├── boxplot_gasto_alojamiento.png")
print(f"    └── dispersion_gente_gastototal.png")
print()
print("  Medidas clave para el informe:")
print(f"    GastoAlojamiento — Media   : {serie_gasto.mean():.2f} USD")
print(f"    GastoAlojamiento — Mediana : {serie_gasto.median():.2f} USD")
print(f"    GastoAlojamiento — Q1      : {Q1:.2f} USD")
print(f"    GastoAlojamiento — Q3      : {Q3:.2f} USD")
print(f"    GastoAlojamiento — IQR     : {IQR:.2f} USD")
print(f"    GastoAlojamiento — Outliers: {len(outliers):,}")
print(f"    Gente vs GastoTotal — r    : {correlacion:.4f}")
print("=" * 65)