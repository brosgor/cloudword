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
git clone <tu-repositorio>
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

1. Edita el array `words` en `cloudword.py` con tu texto
2. Ejecuta el script:
```bash
python cloudword.py
```
3. La nube de palabras se guardará como `nube_palabras.png`

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

El script procesa textos en español y genera nubes de palabras enfocadas en las palabras más significativas, ideal para:

- Análisis de feedback educativo
- Procesamiento de encuestas
- Análisis de contenido textual
- Visualización de temas principales

## Autor

**Alfonso Suárez** (brosgor)  
Email: alfonso.suarez.dev@gmail.com

## Licencia

Este proyecto está bajo la Licencia MIT.
