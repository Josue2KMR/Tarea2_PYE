# Proyecto: Análisis Estadístico de Turismo Emisivo en Uruguay

Este repositorio contiene el código fuente y la documentación correspondiente al trabajo práctico de la asignatura _Probabilidad y Estadística Aplicada_ (Tarea 2). El objetivo es realizar un análisis estadístico completo de los datos de turismo emisivo del Uruguay, obtenidos del Catálogo Nacional de Datos Abiertos del Ministerio de Turismo.

El proyecto está estructurado en tres scripts principales que cubren:

- **Parte 1**: Muestreo aleatorio equiprobable de 2000 registros a partir del dataset original.
- **Parte 2**: Estadística descriptiva (tablas, gráficos, medidas de posición y dispersión).
- **Parte 3**: Inferencia estadística (intervalos de confianza, pruebas de hipótesis, regresión lineal).

Todos los resultados (tablas en consola y gráficos en formato PNG) se generan automáticamente al ejecutar los scripts.

---

## 📁 Estructura del proyecto

```
Tarea2/
├── datos/
│   ├── emisivo.csv               # Archivo original (debe descargarse)
│   └── muestra_2000.csv          # Muestra generada (se crea al ejecutar Parte 1)
├── codigo/
│   ├── parte1_muestreo.py        # Muestreo aleatorio
│   ├── parte2_descriptiva.py     # Estadística descriptiva
│   └── parte3_inferencia.py      # Inferencia estadística
├── resultados/                   # Se crea automáticamente; aquí se guardan los gráficos
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

---


## 📋 Paso a paso para ejecutar manualmente (para profesores y revisores)

Si prefieres ejecutar cada parte por separado o deseas entender el proceso, sigue estos pasos:

### 1. Clonar o descargar el proyecto

Descarga el repositorio y descomprime la carpeta en tu computadora.

### 2. Colocar el archivo de datos

Coloca el archivo `emisivo.csv` (descargado del catálogo) dentro de la carpeta `datos/`.

### 3. Crear y activar un entorno virtual (recomendado)

Abre una terminal (CMD, PowerShell o bash) en la carpeta raíz del proyecto y ejecuta:

```bash
python -m venv venv
```

Activa el entorno virtual:

- **Windows (CMD):** `venv\Scripts\activate.bat`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1` (si da error, ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` una vez)
- **macOS / Linux:** `source venv/bin/activate`

### 4. Instalar las dependencias

Con el entorno virtual activado, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 5. Ejecutar los scripts (opción manual)

Puedes ejecutar cada script por separado desde la raíz del proyecto:

```bash
python codigo/parte1_muestreo.py
python codigo/parte2_descriptiva.py
python codigo/parte3_inferencia.py
```

### 6. Ver los resultados

- Las tablas de frecuencias, intervalos y resultados de tests se imprimen en la consola.
- Los gráficos se guardan en la carpeta `resultados/` con nombres descriptivos:
  - `grafico_destino.png`
  - `histograma_gasto_alojamiento.png`
  - `boxplot_gasto_alojamiento.png`
  - `dispersion_gente_gastototal.png`
  - `regresion_gente_gastototal.png`

---

## 🛠️ Dependencias

El proyecto requiere Python 3.8 o superior y las siguientes librerías (se instalan automáticamente con `pip install -r requirements.txt`):

- `pandas` (manipulación de datos)
- `numpy` (cálculo numérico)
- `matplotlib` (gráficos)
- `scipy` (tests estadísticos)
- `scikit-learn` (regresión lineal)

---

## 📄 Descripción de los scripts

### `parte1_muestreo.py`

- Carga el archivo `emisivo.csv`.
- Selecciona 2000 filas de forma aleatoria sin reposición (equiprobable) usando semilla fija 42.
- Guarda la muestra en `muestra_2000.csv` (sobrescribe si ya existe).
- Muestra información de verificación (columnas, tipos, valores nulos).

### `parte2_descriptiva.py`

- Carga la muestra `muestra_2000.csv`.
- Clasifica las variables solicitadas.
- Genera tabla de frecuencias y gráficos para la variable _Destino_.
- Selecciona la variable _GastoAlojamiento_ y construye:
  - Tabla de frecuencias por intervalos (regla de Sturges).
  - Histograma con líneas de media y mediana, y recuadro con asimetría.
  - Diagrama de cajas (boxplot) horizontal con cuartiles y outliers.
- Genera diagrama de dispersión y calcula correlación entre _Gente_ y _GastoTotal_.

### `parte3_inferencia.py`

- Carga la muestra.
- Calcula intervalos de confianza al 95% para todas las variables de gasto.
- Realiza:
  - Test t de una muestra (cola izquierda) para contrastar si el gasto medio en alojamiento es < 350 USD.
  - Test t pareado para comparar gasto en alimentación vs compras.
  - Test Chi‑cuadrado de independencia entre _Estadía_ (categorizada) y _LugarSalida_ (agrupada).
  - Regresión lineal simple de _GastoTotal_ en función de _Gente_, con interpretación de parámetros y R².
- Genera gráfico de la regresión.

---

## 🔧 Solución de problemas comunes

### Error: `FileNotFoundError: [Errno 2] No such file or directory: 'datos/emisivo.csv'`

Asegúrate de que el archivo `emisivo.csv` esté en la carpeta `datos/`. Si el nombre es diferente, cambia la variable `RUTA_ORIGINAL` en `parte1_muestreo.py`.

### Error al activar el entorno virtual en PowerShell

Ejecuta el siguiente comando una vez y luego intenta activar nuevamente:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Los gráficos no se ven en la consola

Los gráficos se guardan como archivos PNG en la carpeta `resultados/`. Puedes abrirlos con cualquier visor de imágenes.
