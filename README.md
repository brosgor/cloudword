# CloudWord - Generador de Nubes de Palabras con NER

Generador de nubes de palabras en español con procesamiento de lenguaje natural y reconocimiento de entidades nombradas.

## Características

- Procesamiento de lenguaje natural con spaCy
- Reconocimiento de Entidades Nombradas (NER) híbrido (spaCy + regex)
- Detección mejorada de organizaciones colombianas e internacionales
- Filtrado inteligente de stopwords
- Lematización automática
- Nubes de palabras especializadas por tipo de entidad
- Exportación a PNG de alta calidad

## Librerías utilizadas

- **spaCy**: NLP y NER
- **WordCloud**: Generación de nubes
- **Matplotlib**: Visualización
- **pandas**: Manejo de CSV
- **es_core_news_md**: Modelo español (mediano, mejor precisión)

## Instalación

```bash
git clone https://github.com/brosgor/cloudword.git
cd cloudword
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download es_core_news_md
```

## Uso básico

```python
from cloudword import CloudWordAnalyzer

analyzer = CloudWordAnalyzer()

# Desde texto
analyzer.load_document(text="Tu texto aquí")

# Desde CSV
analyzer.load_document(database='datos.csv', column='respuestas')

# Nube tradicional
analyzer.process_text(mode='words')
analyzer.save_wordcloud('nube.png')

# Nube de organizaciones
analyzer.process_text(mode='organizations')
analyzer.save_wordcloud('organizaciones.png')
```

## Reconocimiento de Entidades (NER)

### Tipos de entidades

- **PER**: Personas
- **ORG**: Organizaciones/empresas
- **LOC**: Ubicaciones
- **MISC**: Otras entidades

### Detección híbrida de organizaciones

El sistema combina:
- **NER de spaCy**: Detección automática basada en contexto
- **Patrones regex**: Captura organizaciones específicas:
  - Bancos: "Banco de Bogotá", "Banco de Occidente"
  - Empresas conocidas: IBM, Microsoft, Rappi, Globant, Bancolombia, Ecopetrol
  - Empresas SAS: "Seti SAS", "S4L S.A.S."
  - Universidades: "Universidad Nacional de Colombia"

### Modos de procesamiento

```python
# Palabras tradicionales (sustantivos, adjetivos, verbos)
analyzer.process_text(mode='words')

# Solo organizaciones
analyzer.process_text(mode='organizations')

# Solo personas
analyzer.process_text(mode='persons')

# Solo ubicaciones
analyzer.process_text(mode='locations')

# Limitar a top N entidades
analyzer.process_text(mode='organizations', top_n=20)
```

### Stopwords personalizadas

```python
# Agregar stopwords adicionales (se suman a las default)
analyzer = CloudWordAnalyzer(custom_stopwords={'DevOps', 'Intern', 'startup'})

# Las stopwords se aplican inteligentemente:
# - Palabras individuales: se filtran
# - Frases completas: solo si coinciden exactamente
```

## Modelos disponibles

```bash
# Pequeño (más rápido, menos preciso)
python -m spacy download es_core_news_sm
analyzer = CloudWordAnalyzer(model='es_core_news_sm')

# Mediano (balanceado) - RECOMENDADO Y POR DEFECTO
python -m spacy download es_core_news_md

# Grande (más lento, máxima precisión)
python -m spacy download es_core_news_lg
analyzer = CloudWordAnalyzer(model='es_core_news_lg')
```

## Limitaciones

- NER no detecta cargos ("CEO", "Director") - se filtran automáticamente
- Mejor precisión con modelo `md` o `lg`
- Regex complementario optimizado para organizaciones colombianas

## Autor

Luis Pedraos (brosgor)

## Licencia

GPL v3
