# Análisis Estadístico del Turismo Emisivo en Uruguay

Trabajo práctico de **Probabilidad y Estadística Aplicada — Tarea 2**  
Facultad de Ingeniería y Tecnologías · Universidad Católica del Uruguay

Análisis estadístico completo de los datos de turismo emisivo del Uruguay, obtenidos del [Catálogo Nacional de Datos Abiertos](https://catalogodatos.gub.uy/dataset/ministerio-de-turismo-turismo-emisivo) del Ministerio de Turismo.

---

## 📁 Estructura del proyecto

```
Tarea2/
├── .gitignore
├── README.md
├── requirements.txt
├── codigo/
│   ├── parte1_muestreo.py        # Muestreo aleatorio equiprobable (2.000 registros)
│   ├── parte2_descriptiva.py     # Estadística descriptiva: tablas, gráficos, medidas
│   └── parte3_inferencia.py      # Inferencia: IC, hipótesis, chi-cuadrado, regresión
├── datos/
│   ├── emisivo.csv               # Dataset original — debe descargarse (ver más abajo)
│   └── muestra_2000.csv          # Generado al ejecutar parte1_muestreo.py
├── resultados/                   # Generado automáticamente al correr los scripts
│   ├── grafico_destino.png
│   ├── histograma_gasto_alojamiento.png
│   ├── boxplot_gasto_alojamiento.png
│   ├── dispersion_gente_gastototal.png
│   └── regresion_gente_gastototal.png
└── informe/
    └── informe_turismo_emisivo_T2.docx
```

> **Nota:** `venv/` no se incluye en el repositorio. Cada usuario debe crearlo localmente siguiendo las instrucciones de abajo.

---

## ⚙️ Requisitos previos

- Python **3.8 o superior**
- pip (incluido con Python)
- El archivo `emisivo.csv` descargado y colocado en `datos/`

### Descargar el dataset

1. Ir a: <https://catalogodatos.gub.uy/dataset/ministerio-de-turismo-turismo-emisivo>
2. Descargar el archivo `emisivo.csv`
3. Colocarlo en la carpeta `datos/` del proyecto

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tarea2.git
cd tarea2
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

| Sistema              | Comando                     |
| -------------------- | --------------------------- |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
| Windows (CMD)        | `venv\Scripts\activate.bat` |
| macOS / Linux        | `source venv/bin/activate`  |

> **PowerShell:** si aparece error de permisos, ejecutar una sola vez:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar los scripts en orden

```bash
python codigo/parte1_muestreo.py
python codigo/parte2_descriptiva.py
python codigo/parte3_inferencia.py
```

Los tres scripts deben ejecutarse **desde la raíz del proyecto** (donde está el `README.md`), no desde dentro de `codigo/`.

---

## 📊 Resultados

Cada script imprime sus resultados en la consola y genera los archivos correspondientes:

| Script                  | Salidas en consola                                  | Archivos generados          |
| ----------------------- | --------------------------------------------------- | --------------------------- |
| `parte1_muestreo.py`    | Dimensiones del dataset, verificación de la muestra | `datos/muestra_2000.csv`    |
| `parte2_descriptiva.py` | Tablas de frecuencias, cuartiles, correlación       | 4 gráficos en `resultados/` |
| `parte3_inferencia.py`  | IC, estadísticos t, χ², parámetros de regresión     | 1 gráfico en `resultados/`  |

---

## 🛠️ Dependencias

| Librería       | Versión | Uso                                  |
| -------------- | ------- | ------------------------------------ |
| `pandas`       | 2.2.2   | Manipulación de datos tabulares      |
| `numpy`        | 1.26.4  | Operaciones numéricas                |
| `matplotlib`   | 3.9.0   | Generación de gráficos               |
| `scipy`        | 1.13.1  | Tests estadísticos (t, chi-cuadrado) |
| `scikit-learn` | 1.5.0   | Regresión lineal                     |

---

## ❓ Problemas frecuentes

**`FileNotFoundError: datos/emisivo.csv`**  
→ El archivo no está en la carpeta `datos/`. Descargarlo del catálogo y colocarlo ahí.

**`FileNotFoundError: datos/muestra_2000.csv`**  
→ Ejecutar primero `parte1_muestreo.py` antes de correr la Parte 2 o la Parte 3.

**Los gráficos no aparecen en pantalla**  
→ Se guardan automáticamente en `resultados/`. Abrirlos desde el explorador de archivos.

**Error al activar el entorno virtual en PowerShell**  
→ Ejecutar `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` y volver a intentar.
