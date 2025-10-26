# CloudWord - Generador de Nubes de Palabras con NER

Generador de nubes de palabras en español con procesamiento de lenguaje natural y reconocimiento de entidades nombradas.

## Características

- Procesamiento de lenguaje natural con spaCy
- Reconocimiento de Entidades Nombradas (NER)
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

analyzer = CloudWordAnalyzer()  # Usa es_core_news_md por defecto

# Desde texto
analyzer.load_document(text="Tu texto aquí")

# Desde CSV
analyzer.load_document(database='datos.csv', column='respuestas')

# Nube tradicional
analyzer.process_text()
analyzer.save_wordcloud('nube.png')
```

## Reconocimiento de Entidades (NER)

### Tipos de entidades

- **PER**: Personas
- **ORG**: Organizaciones/empresas
- **LOC**: Ubicaciones
- **MISC**: Otras entidades

### Extraer entidades

```python
# Todas las entidades
entidades = analyzer.extract_entities()

# Solo organizaciones
orgs = analyzer.extract_entities(entity_types=['ORG'])

# Con conteo
conteos = analyzer.get_entity_counts()
```

### Métodos específicos

```python
# Top 10 organizaciones
top_orgs = analyzer.get_organizations(top_n=10)

# Todas las personas
personas = analyzer.get_persons()

# Top 5 ubicaciones
lugares = analyzer.get_locations(top_n=5)

# Resumen en consola
analyzer.print_entity_summary()
```

### Nubes de palabras por entidad

```python
# Solo organizaciones
wc_orgs = analyzer.generate_entity_wordcloud(entity_type='ORG')
analyzer.save_wordcloud('empresas.png', wordcloud=wc_orgs)

# Solo personas
wc_per = analyzer.generate_entity_wordcloud(entity_type='PER')
analyzer.save_wordcloud('personas.png', wordcloud=wc_per)

# Solo ubicaciones
wc_loc = analyzer.generate_entity_wordcloud(entity_type='LOC')
analyzer.save_wordcloud('lugares.png', wordcloud=wc_loc)
```

## Personalización

```python
# Stopwords personalizados
custom = {'palabra1', 'palabra2'}
analyzer = CloudWordAnalyzer(custom_stopwords=custom)

# Filtros POS
analyzer.process_text(pos_filter=['NOUN'])  # Solo sustantivos
analyzer.process_text(pos_filter=['NOUN', 'ADJ'])  # Sustantivos y adjetivos

# WordCloud personalizado
wc = analyzer.generate_entity_wordcloud(
    entity_type='ORG',
    width=1200,
    height=600,
    background_color='black',
    colormap='viridis'
)
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

- NER no detecta cargos ("CEO", "Director")
- Mejor precisión con texto que mantiene mayúsculas

## Autor

Luis Pedraos (brosgor)

## Licencia

GPL v3
