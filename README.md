# CloudWord - Generador de Nubes de Palabras

Un generador de nubes de palabras en español que utiliza procesamiento de lenguaje natural avanzado para crear visualizaciones significativas de texto.

## Características

- **Procesamiento de lenguaje natural**: Utiliza spaCy para análisis morfológico avanzado
- **Filtrado inteligente**: Elimina automáticamente stopwords, puntuación y palabras irrelevantes
- **Lematización**: Convierte palabras a su forma base para evitar duplicados
- **Filtrado por categoría**: Solo conserva sustantivos, adjetivos y verbos relevantes
- **Exportación a imagen**: Genera archivos PNG de alta calidad

## Librerías utilizadas

- **spaCy**: Procesamiento de lenguaje natural avanzado
- **WordCloud**: Generación de nubes de palabras
- **Matplotlib**: Visualización y exportación de imágenes
- **es_core_news_sm**: Modelo de español para spaCy

## Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/brosgor/cloudword.git
cd cloudword
```

### 2. Crear entorno virtual
```bash
python3 -m venv .venv
```

### 3. Activar el entorno virtual
```bash
# En Linux/macOS:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Descargar modelo de español para spaCy
```bash
python -m spacy download es_core_news_sm
```

## Uso

Existen **dos formas** de generar nubes de palabras con este proyecto:

### Método 1: Pegar texto directamente

1. Abre el archivo `cloudword.py`
2. En la función `getDocument()`, modifica el texto entre las comillas triples:
```python
words = getDocument()  # Sin parámetros
```
3. Edita el texto en la línea 11:
```python
words = [
    """
    Aquí va el texto del cual quieres generar la nube de palabras.
    """
]
```
4. Ejecuta el script:
```bash
python cloudword.py
```

### Método 2: Analizar datos desde un archivo CSV

1. Asegúrate de tener tu archivo CSV en el directorio del proyecto
2. En `cloudword.py`, modifica la llamada a `getDocument()` especificando el archivo y columna:
```python
words = getDocument(database='tu_archivo.csv', column='Nombre_de_la_Columna')
```
3. Ejecuta el script:
```bash
python cloudword.py
```

**Ejemplo con CSV:**
```python
words = getDocument(database='estudiantes.csv', column='Justifique la respuesta anterior (¿Por qué ?)')
```

### Resultado

En ambos casos, la nube de palabras se guardará automáticamente como `nube_palabras.png` en el directorio del proyecto.

## Estructura del proyecto

```
cloudword/
├── .venv/              # Entorno virtual
├── cloudword.py        # Script principal
├── requirements.txt    # Dependencias
├── README.md          # Documentación
└── nube_palabras.png  # Imagen generada
```

## Ejemplo de uso

El script procesa textos en español y genera nubes de palabras enfocadas en las palabras más significativas. Soporta dos métodos de entrada:

1. **Texto directo**: Pega tu contenido directamente en el código
2. **Análisis de CSV**: Procesa columnas de archivos CSV, ideal para:
   - Análisis de feedback educativo
   - Procesamiento de encuestas masivas
   - Análisis de respuestas abiertas
   - Visualización de temas principales en datasets

## Autor

**Alfonso Suárez** (brosgor)  

## Licencia

Este proyecto está bajo la Licencia GPL v3. Consulta el archivo [LICENSE](LICENSE) para más detalles.
