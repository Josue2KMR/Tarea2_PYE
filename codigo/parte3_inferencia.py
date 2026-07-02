# =============================================================================
# Estudio Estadístico de la Demanda Turística Emisiva Uruguaya
# Probabilidad y Estadística Aplicada — Facultad de Ingeniería y Tecnologías
#
# PARTE 3: Inferencia Estadística
#
# Descripción:
#   Este script realiza el análisis inferencial completo sobre la muestra de
#   2,000 observaciones del dataset de Turismo Emisivo del Uruguay, publicado
#   por el Ministerio de Turismo en el catálogo de datos abiertos del gobierno.
#
#   Contexto de investigación:
#   A partir de la muestra seleccionada en la Parte 1, se busca ir más allá
#   de la descripción de los datos y realizar afirmaciones estadísticas sobre
#   la POBLACIÓN de turistas emisivos uruguayos. Para ello se emplean tres
#   herramientas clásicas de inferencia: intervalos de confianza (estimación
#   de parámetros), tests de hipótesis (verificación de afirmaciones) y
#   regresión lineal (modelado de relaciones entre variables).
#
#   Contenido:
#     3.1 — Intervalos de confianza para la media de cada variable de Gasto
#     3.2 — Test t de una muestra: ¿GastoAlojamiento medio < $350 USD?
#     3.3 — Test t de dos muestras: ¿GastoAlimentacion > GastoCompras?
#     3.4 — Test Chi-cuadrado: independencia entre Estadía y LugarSalida
#     3.5 — Regresión Lineal Simple: GastoTotal en función de Gente
#
# Requisitos:
#   Instalar dependencias desde la raíz del proyecto:
#     pip install -r requirements.txt
#
# Uso:
#   Desde la raíz del proyecto ejecutar:
#     python codigo/parte3_inferencia.py
# =============================================================================

# --- Importación de librerías ------------------------------------------------
import pandas as pd                          # Manipulación de datos
import numpy as np                           # Operaciones numéricas
import matplotlib.pyplot as plt             # Gráficos
import matplotlib.ticker as mticker
import os

from scipy import stats                      # Tests estadísticos (t, chi2)
from scipy.stats import t as t_dist         # Distribución t de Student
from sklearn.linear_model import LinearRegression   # Regresión lineal
from sklearn.metrics import r2_score        # Coeficiente de determinación R²

# --- Configuración general ---------------------------------------------------
RUTA_MUESTRA    = os.path.join("datos", "muestra_2000.csv")
RUTA_RESULTADOS = "resultados"
ALFA            = 0.05        # Nivel de significación para todos los tests
CONFIANZA       = 1 - ALFA    # Nivel de confianza: 95%

os.makedirs(RUTA_RESULTADOS, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "sans-serif",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

print("=" * 65)
print("PARTE 3 - Inferencia Estadística — Turismo Emisivo Uruguay")
print("=" * 65)

# --- Carga de datos ----------------------------------------------------------
df = pd.read_csv(RUTA_MUESTRA)
print(f"\n[Carga] muestra_2000.csv → {len(df):,} filas | {df.shape[1]} columnas")

# Variables de gasto disponibles en el dataset
VARS_GASTO = [
    "GastoAlojamiento",
    "GastoAlimentacion",
    "GastoTransporteInternac",
    "GatoTransporteLocal",    # Nota: nombre con error tipográfico en la fuente
    "GastoCultural",
    "GastoTours",
    "GastoCompras",
    "GastoResto",
]


# =============================================================================
# ÍTEM 3.1 — Intervalos de confianza para la media de cada variable de Gasto
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 3.1 — Intervalos de confianza al 95% para variables de Gasto")
print("─" * 65)

# Un intervalo de confianza al (1-α)·100% para la media poblacional μ se
# construye como:
#
#   IC = [ x̄ - t_(α/2, n-1) · (s/√n) ,  x̄ + t_(α/2, n-1) · (s/√n) ]
#
# donde:
#   x̄  = media muestral
#   s   = desviación estándar muestral (con corrección de Bessel, ddof=1)
#   n   = tamaño de la muestra
#   t_(α/2, n-1) = cuantil de la distribución t de Student con n-1 grados de libertad
#
# Se usa la distribución t (en lugar de z) porque la varianza poblacional es
# desconocida y debe estimarse a partir de la muestra.

print(f"\nNivel de confianza: {CONFIANZA*100:.0f}%  |  α = {ALFA}  |  n = {len(df):,}\n")

resultados_ic = []

for var in VARS_GASTO:
    serie = df[var].dropna()
    n     = len(serie)
    media = serie.mean()
    std   = serie.std(ddof=1)              # Desviación estándar muestral
    se    = std / np.sqrt(n)              # Error estándar de la media

    # Valor crítico de t para α/2 con n-1 grados de libertad
    t_critico = t_dist.ppf(1 - ALFA / 2, df=n - 1)

    lim_inf = media - t_critico * se
    lim_sup = media + t_critico * se

    resultados_ic.append({
        "Variable"       : var,
        "Media (x̄)"     : round(media, 4),
        "Desv. Est. (s)" : round(std, 4),
        "Error Est. (se)": round(se, 4),
        "t crítico"      : round(t_critico, 4),
        "Límite inf."    : round(lim_inf, 4),
        "Límite sup."    : round(lim_sup, 4),
    })

tabla_ic = pd.DataFrame(resultados_ic)
print(tabla_ic.to_string(index=False))

print("\n  Conclusiones sobre los valores obtenidos:")
print("  Los rubros con medias más altas son GastoAlojamiento (~316 USD)")
print("  y GastoTransporteInternac (~311 USD), lo que refleja que hospedaje")
print("  y traslado son los costos dominantes del viaje al exterior.")
print("  GastoAlimentacion (~266 USD) y GastoCompras (~254 USD) son")
print("  similares entre sí, lo que es consistente con el resultado del")
print("  test t pareado (ítem 3.3): no hay diferencia significativa entre ambos.")
print("  En contraste, GastoTours (~5 USD) y GastoCultural (~82 USD)")
print("  son muy bajos, sugiriendo que el viajero uruguayo no prioriza")
print("  el turismo organizado ni las actividades culturales pagas.")
print("  La alta desviación estándar de GastoTransporteInternac (824 USD)")
print("  revela gran heterogeneidad: vuelos intercontinentales conviven con")
print("  cruces terrestres de bajo costo en la misma muestra.")


# =============================================================================
# ÍTEM 3.2 — Test t de una muestra: ¿GastoAlojamiento medio < $350 USD?
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 3.2 — Test t (una muestra): ¿GastoAlojamiento medio < 350 USD?")
print("─" * 65)

# Formulación del test de hipótesis:
#
#   H₀: μ_alojamiento ≥ 350   (la media poblacional es al menos 350 USD)
#   H₁: μ_alojamiento < 350   (la media poblacional es menor a 350 USD)
#
# Es un test UNILATERAL a la izquierda (cola izquierda), ya que la hipótesis
# alternativa plantea que el parámetro es MENOR a un valor específico.
#
# Estadístico del test:
#   t = (x̄ - μ₀) / (s / √n)
#
# Se rechaza H₀ si:  p-valor < α  (usando cola izquierda)

MU_0 = 350   # Valor hipotético bajo H₀
serie_aloj = df["GastoAlojamiento"].dropna()

# stats.ttest_1samp realiza el test bilateral por defecto.
# Para obtener la cola izquierda dividimos el p-valor bilateral por 2
# solo cuando el estadístico t es negativo (x̄ < μ₀).
t_stat, p_bilateral = stats.ttest_1samp(serie_aloj, popmean=MU_0)

# P-valor para la hipótesis alternativa H₁: μ < μ₀ (cola izquierda)
if t_stat < 0:
    p_valor = p_bilateral / 2
else:
    p_valor = 1 - p_bilateral / 2

conclusion = "Se RECHAZA H₀" if p_valor < ALFA else "NO se rechaza H₀"

print(f"\n  H₀: μ_alojamiento ≥ {MU_0} USD")
print(f"  H₁: μ_alojamiento < {MU_0} USD  (cola izquierda)")
print(f"  α  = {ALFA}")
print(f"\n  Media muestral  : {serie_aloj.mean():.4f} USD")
print(f"  Estadístico t   : {t_stat:.4f}")
print(f"  P-valor (izq.)  : {p_valor:.4f}")
print(f"\n  Conclusión: {conclusion}")
if p_valor < ALFA:
    print(f"  → Con α={ALFA}, hay evidencia estadística suficiente para afirmar")
    print(f"    que los uruguayos gastan en promedio MENOS de ${MU_0} USD en alojamiento.")
else:
    print(f"  → Con α={ALFA}, NO hay evidencia estadística suficiente para afirmar")
    print(f"    que los uruguayos gastan en promedio MENOS de ${MU_0} USD en alojamiento.")


# =============================================================================
# ÍTEM 3.3 — Test t de dos muestras: ¿GastoAlimentacion > GastoCompras?
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 3.3 — Test t (dos muestras): ¿GastoAlimentacion > GastoCompras?")
print("─" * 65)

# Las dos muestras son PAREADAS: cada fila representa al mismo grupo de
# viajeros, por lo que el gasto en alimentación y en compras de un mismo
# registro están relacionados. Se aplica el test t de muestras pareadas.
#
# Formulación:
#   Definimos d_i = GastoAlimentacion_i - GastoCompras_i
#
#   H₀: μ_d ≤ 0   (en promedio no se gasta más en alimentación que en compras)
#   H₁: μ_d > 0   (en promedio se gasta MÁS en alimentación que en compras)
#
# Es un test unilateral a la derecha.

alim   = df["GastoAlimentacion"].dropna()
compras = df["GastoCompras"].dropna()

# Alineamos índices para el test pareado
idx_comun = alim.index.intersection(compras.index)
alim_p    = alim.loc[idx_comun]
compras_p = compras.loc[idx_comun]

t_stat3, p_bilateral3 = stats.ttest_rel(alim_p, compras_p)

# P-valor para cola derecha (H₁: μ_d > 0)
if t_stat3 > 0:
    p_valor3 = p_bilateral3 / 2
else:
    p_valor3 = 1 - p_bilateral3 / 2

conclusion3 = "Se RECHAZA H₀" if p_valor3 < ALFA else "NO se rechaza H₀"

print(f"\n  H₀: μ_alimentacion ≤ μ_compras   (diferencia ≤ 0)")
print(f"  H₁: μ_alimentacion >  μ_compras   (diferencia > 0, cola derecha)")
print(f"  α  = {ALFA}")
print(f"\n  Media GastoAlimentacion : {alim_p.mean():.4f} USD")
print(f"  Media GastoCompras      : {compras_p.mean():.4f} USD")
print(f"  Diferencia media (d̄)   : {(alim_p - compras_p).mean():.4f} USD")
print(f"  Estadístico t           : {t_stat3:.4f}")
print(f"  P-valor (der.)          : {p_valor3:.4f}")
print(f"\n  Conclusión: {conclusion3}")
if p_valor3 < ALFA:
    print(f"  → Con α={ALFA}, hay evidencia estadística para afirmar que los")
    print(f"    uruguayos gastan MÁS en alimentación que en compras al viajar.")
else:
    print(f"  → Con α={ALFA}, NO hay evidencia estadística suficiente para afirmar")
    print(f"    que los uruguayos gastan más en alimentación que en compras.")


# =============================================================================
# ÍTEM 3.4 — Test Chi-cuadrado: independencia entre Estadía y LugarSalida
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 3.4 — Test Chi-cuadrado: Estadía vs LugarSalida")
print("─" * 65)

# El test Chi-cuadrado de independencia evalúa si dos variables categóricas
# están relacionadas o son independientes.
#
# Como Estadía es una variable numérica discreta (días), la categorizamos
# en grupos con sentido turístico para poder aplicar el test:
#   • Corta   : 1 a 7 días   (viaje de una semana o menos)
#   • Mediana : 8 a 14 días  (hasta dos semanas)
#   • Larga   : 15 días o más
#
# Formulación:
#   H₀: Estadía y LugarSalida son INDEPENDIENTES
#   H₁: Estadía y LugarSalida NO son independientes (existe asociación)

bins_estadia  = [0, 7, 14, float("inf")]
etiq_estadia  = ["Corta (1-7 días)", "Mediana (8-14 días)", "Larga (15+ días)"]

df["EstadiaCateg"] = pd.cut(
    df["Estadia"],
    bins=bins_estadia,
    labels=etiq_estadia,
    right=True,
    include_lowest=True
)

# Agrupamos lugares de salida con menos de 30 observaciones en "Otros"
# para evitar frecuencias esperadas muy bajas (requisito del test Chi²)
conteo_lugar = df["Lugar Salida"].value_counts()
lugares_frecuentes = conteo_lugar[conteo_lugar >= 30].index
df["LugarSalidaAgrup"] = df["Lugar Salida"].apply(
    lambda x: x if x in lugares_frecuentes else "Otros"
)

# Construimos la tabla de contingencia.
# pd.crosstab ordena las columnas alfabéticamente, lo que deja "Otros" en el
# medio. Lo reordenamos para que "Otros" aparezca siempre en la última columna,
# antes del total, ya que es una categoría residual y debe ir al final.
tabla_cont = pd.crosstab(df["EstadiaCateg"], df["LugarSalidaAgrup"])
cols_ordenadas = [c for c in sorted(tabla_cont.columns) if c != "Otros"] + ["Otros"]
tabla_cont = tabla_cont[cols_ordenadas]

print("\n  Tabla de contingencia (Estadía × LugarSalida):")
print(tabla_cont.to_string())

# Aplicamos el test Chi-cuadrado
chi2, p_chi2, gl, frec_esperadas = stats.chi2_contingency(tabla_cont)

# Verificación del supuesto: todas las frecuencias esperadas deben ser ≥ 5
min_esperada = frec_esperadas.min()
supuesto_ok  = min_esperada >= 5

conclusion4 = "Se RECHAZA H₀" if p_chi2 < ALFA else "NO se rechaza H₀"

print(f"\n  H₀: Estadía y LugarSalida son independientes")
print(f"  H₁: Estadía y LugarSalida NO son independientes")
print(f"  α  = {ALFA}")
print(f"\n  Estadístico χ²          : {chi2:.4f}")
print(f"  Grados de libertad (gl) : {gl}")
print(f"  P-valor                 : {p_chi2:.4f}")
print(f"  Frec. esperada mínima   : {min_esperada:.2f}  "
      f"({'✓ supuesto OK' if supuesto_ok else '✗ supuesto no cumplido'})")
print(f"\n  Conclusión: {conclusion4}")
if p_chi2 < ALFA:
    print(f"  → Con α={ALFA}, hay evidencia de que la duración de la estadía")
    print(f"    y el lugar de salida NO son independientes (existe asociación).")
else:
    print(f"  → Con α={ALFA}, NO hay evidencia suficiente para afirmar que")
    print(f"    la duración de la estadía y el lugar de salida estén asociados.")


# =============================================================================
# ÍTEM 3.5 — Regresión Lineal Simple: GastoTotal ~ Gente
# =============================================================================
print("\n" + "─" * 65)
print("ÍTEM 3.5 — Regresión Lineal Simple: GastoTotal ~ Gente")
print("─" * 65)

# La regresión lineal simple busca modelar la relación entre dos variables
# mediante una recta de la forma:
#
#   ŷ = β₀ + β₁·x
#
# donde:
#   ŷ  = GastoTotal estimado (variable dependiente / respuesta)
#   x  = Gente (variable independiente / predictora)
#   β₀ = intercepto (valor estimado de ŷ cuando x = 0)
#   β₁ = pendiente (cambio esperado en ŷ por cada unidad adicional de x)
#
# El coeficiente de determinación R² indica qué proporción de la variabilidad
# del GastoTotal es explicada por la cantidad de personas (Gente).

X = df[["Gente"]].values    # Variable independiente (matriz columna)
y = df["GastoTotal"].values  # Variable dependiente (vector)

modelo = LinearRegression()
modelo.fit(X, y)

beta_0  = modelo.intercept_            # Intercepto β₀
beta_1  = modelo.coef_[0]             # Pendiente β₁
y_pred  = modelo.predict(X)           # Valores estimados por el modelo
r2      = r2_score(y, y_pred)         # Coeficiente de determinación R²
r       = np.sqrt(r2) * np.sign(beta_1)  # Coeficiente de correlación r

# Test de significancia de la pendiente (H₀: β₁ = 0)
n_reg    = len(y)
residuos = y - y_pred
sse      = np.sum(residuos ** 2)                     # Suma cuadrados error
sxx      = np.sum((X.flatten() - X.mean()) ** 2)    # Suma cuadrados de X
se_b1    = np.sqrt(sse / (n_reg - 2) / sxx)         # Error estándar de β₁
t_b1     = beta_1 / se_b1                            # Estadístico t de β₁
p_b1     = 2 * (1 - t_dist.cdf(abs(t_b1), df=n_reg - 2))   # P-valor bilateral

print(f"\n  Modelo ajustado: GastoTotal = {beta_0:.4f} + {beta_1:.4f} · Gente")
print(f"\n  Parámetros del modelo:")
print(f"    β₀ (intercepto)     = {beta_0:.4f} USD")
print(f"    β₁ (pendiente)      = {beta_1:.4f} USD por persona")
print(f"    R²                  = {r2:.4f}  ({r2*100:.2f}%)")
print(f"    r (correlación)     = {r:.4f}")
print(f"\n  Test de significancia de β₁:")
print(f"    H₀: β₁ = 0  (Gente no explica el GastoTotal)")
print(f"    H₁: β₁ ≠ 0  (Gente SÍ tiene efecto sobre GastoTotal)")
print(f"    Estadístico t : {t_b1:.4f}")
print(f"    P-valor       : {p_b1:.4f}")
print(f"    Conclusión    : {'Se RECHAZA H₀ — β₁ es significativo' if p_b1 < ALFA else 'NO se rechaza H₀'}")

print(f"\n  Interpretación:")
print(f"    • Por cada persona adicional en el grupo, el GastoTotal esperado")
print(f"      aumenta en {beta_1:.2f} USD.")
print(f"    • R² = {r2:.4f} significa que la variable Gente, como único predictor,")
print(f"      explica el {r2*100:.2f}% de la variabilidad del GastoTotal.")
print(f"    • IMPORTANTE — significancia estadística vs. bondad de ajuste:")
print(f"      El test t de β₁ (t={t_b1:.2f}, p≈0) indica que la pendiente es")
print(f"      estadísticamente distinta de cero: Gente SÍ tiene un efecto real")
print(f"      sobre GastoTotal. Esto no contradice el R² bajo. Con n=2.000,")
print(f"      efectos pequeños se detectan con alta potencia estadística,")
print(f"      pero eso no implica que el modelo explique bien la variabilidad.")
print(f"      En síntesis: Gente influye en el gasto, pero la mayor parte de")
print(f"      la variación se debe a factores no incluidos en este modelo")
print(f"      (destino, duración, tipo de alojamiento). Un modelo de regresión")
print(f"      múltiple con esas variables mejoraría sustancialmente el R².")

# Gráfico: dispersión + recta de regresión
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(X, y, alpha=0.3, s=18, color="#2c7bb6",
           edgecolors="none", label="Observaciones")
x_line = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
ax.plot(x_line, modelo.predict(x_line), color="#d7191c", linewidth=2.5,
        label=f"ŷ = {beta_0:.0f} + {beta_1:.0f}·Gente  (R² = {r2:.4f})")
ax.set_title(
    "Regresión Lineal Simple — GastoTotal en función de Gente\n"
    "(Muestra n = 2,000 — Turismo Emisivo Uruguay)",
    fontweight="bold"
)
ax.set_xlabel("Cantidad de personas en el grupo (Gente)")
ax.set_ylabel("Gasto Total del grupo (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend(fontsize=10)
plt.tight_layout()
ruta_reg = os.path.join(RUTA_RESULTADOS, "regresion_gente_gastototal.png")
plt.savefig(ruta_reg, bbox_inches="tight")
plt.close()
print(f"\n  Gráfico guardado: {ruta_reg}")


# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 65)
print("RESUMEN — Parte 3 completada")
print("=" * 65)
print("\n  Resultados clave para el informe:\n")
print(f"  [3.1] IC al 95% calculados para {len(VARS_GASTO)} variables de gasto.")
print(f"  [3.2] Test t (1 muestra)  → t={t_stat:.4f} | p={p_valor:.4f} | {conclusion}")
print(f"  [3.3] Test t (2 muestras) → t={t_stat3:.4f} | p={p_valor3:.4f} | {conclusion3}")
print(f"  [3.4] Chi-cuadrado        → χ²={chi2:.4f} | p={p_chi2:.4f} | {conclusion4}")
print(f"  [3.5] Regresión lineal    → β₁={beta_1:.4f} | R²={r2:.4f} | "
      f"{'β₁ significativo' if p_b1 < ALFA else 'β₁ no significativo'}")
print(f"\n  Gráfico generado: {ruta_reg}")
print("=" * 65)