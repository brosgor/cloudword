from wordcloud import WordCloud
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


class CloudWordAnalyzer:
    """
    Clase para analizar texto y generar nubes de palabras usando spaCy y WordCloud.
    """
    
    def __init__(self, model='es_core_news_md', custom_stopwords=None):
        """
        Inicializa el analizador con el modelo de spaCy y stopwords personalizados.
        
        Args:
            model: Nombre del modelo de spaCy a cargar
            custom_stopwords: Set de palabras adicionales a excluir (se agregan a las default)
        """
        self.nlp = spacy.load(model)
        
        # Stopwords por defecto
        default_stopwords = {
            'puede', 'pueden', 'debe', 'deben', 'hace', 'hacen', 
            'dice', 'dicen', 'vez', 'veces', 'forma', 'manera',
            'través', 'ejemplo', 'casos', 'caso', 'tipo', 'tipos',
            'parte', 'partes', 'lugar', 'lugares', 'tiempo', 'momento',
            'programa', 'universidad', 'pregrado', 'carrera', 'problema', 
            'estudiante', 'universitario', 'el', 'él', 'necesario', 
            'permitir', 'engineer', 'developer', 'empresa', 'sa', 'docente',
        }
        
        # Combinar default con las personalizadas
        if custom_stopwords:
            self.custom_stopwords = default_stopwords.union(custom_stopwords)
        else:
            self.custom_stopwords = default_stopwords
            
        self._add_custom_stopwords()
        self.document = None
        self.filtered_text = None
        self.entity_frequencies = None  # Para almacenar frecuencias de entidades
        self.doc = None  # Guardamos el documento procesado por spaCy
        
    def _add_custom_stopwords(self):
        """Añade las stopwords personalizadas al vocabulario de spaCy."""
        for word in self.custom_stopwords:
            self.nlp.vocab[word].is_stop = True
            lexeme = self.nlp.vocab[word]
            lexeme.is_stop = True
    
    def load_document(self, database=None, column=None, text=None):
        """
        Carga el documento desde un CSV o desde texto directo.
        
        Args:
            database: Ruta al archivo CSV
            column: Nombre o índice de la columna a usar
            text: Texto directo (alternativa a database/column)
        
        Returns:
            str: El documento cargado
        """
        if text is not None:
            self.document = text
        elif database is None or column is None:
            self.document = ""
            print("⚠️ No se proporcionó fuente de datos. Documento vacío.")
        else:
            df = pd.read_csv(database)
            
            # Verificar columnas duplicadas
            if df.columns.duplicated().any():
                print("⚠️ ADVERTENCIA: El CSV tiene columnas duplicadas:")
                duplicated_cols = df.columns[df.columns.duplicated()].tolist()
                print(f"Columnas duplicadas: {duplicated_cols}")
            
            # Selección por índice o nombre
            if isinstance(column, int):
                self.document = df.iloc[:, column].astype(str).str.cat(sep=' ')
                print(f"✓ Usando columna #{column}: '{df.columns[column]}'")
            else:
                self.document = df[column].astype(str).str.cat(sep=' ')
                print(f"✓ Usando columna: '{column}'")
        
        return self.document
    
    def process_text(self, mode='words', pos_filter=None, top_n=None):
        """
        Procesa el texto con diferentes modos de análisis.
        
        Args:
            mode: Modo de procesamiento
                - 'words': Palabras filtradas tradicional (default)
                - 'organizations': Solo organizaciones
                - 'persons': Solo personas
                - 'locations': Solo ubicaciones
            pos_filter: Lista de POS tags a mantener (solo para mode='words')
                       Default: ['NOUN', 'ADJ', 'VERB']
            top_n: Limitar a las top N entidades (solo para modos de entidades)
        
        Returns:
            str: Texto filtrado procesado
        """
        if self.document is None:
            raise ValueError("Primero debes cargar un documento con load_document()")
        
        # MODO: Palabras tradicionales
        if mode == 'words':
            if pos_filter is None:
                pos_filter = ['NOUN', 'ADJ', 'VERB']
            
            doc_lower = self.nlp(self.document.lower())
            filtered_words = []
            
            for token in doc_lower:
                if (not token.is_stop and
                    token.lemma_.lower() not in self.custom_stopwords and
                    token.text.lower() not in self.custom_stopwords and
                    not token.is_punct and
                    not token.is_space and
                    len(token.text) > 2 and
                    token.pos_ in pos_filter and
                    token.text.isalpha()):
                    filtered_words.append(token.lemma_)
            
            self.filtered_text = " ".join(filtered_words)
        
        # MODO: Organizaciones
        elif mode == 'organizations':
            orgs = self.get_organizations(top_n=top_n)
            # Guardar frecuencias limpias para generate_from_frequencies()
            self.entity_frequencies = {}
            for org, count in orgs.items():
                clean_org = ' '.join(org.split())
                if clean_org:
                    self.entity_frequencies[clean_org] = self.entity_frequencies.get(clean_org, 0) + count
            # Marcar que usamos modo entidades
            self.filtered_text = None
        
        # MODO: Personas
        elif mode == 'persons':
            persons = self.get_persons(top_n=top_n)
            self.entity_frequencies = {}
            for person, count in persons.items():
                clean_person = ' '.join(person.split())
                if clean_person:
                    self.entity_frequencies[clean_person] = self.entity_frequencies.get(clean_person, 0) + count
            self.filtered_text = None
        
        # MODO: Ubicaciones
        elif mode == 'locations':
            locations = self.get_locations(top_n=top_n)
            self.entity_frequencies = {}
            for loc, count in locations.items():
                clean_loc = ' '.join(loc.split())
                if clean_loc:
                    self.entity_frequencies[clean_loc] = self.entity_frequencies.get(clean_loc, 0) + count
            self.filtered_text = None
        
        else:
            raise ValueError(f"Modo '{mode}' no válido. Usa: 'words', 'organizations', 'persons', 'locations'")
        
        return self.filtered_text
    
    def extract_entities(self, entity_types=None):
        """
        Extrae entidades nombradas (NER) del documento.
        
        Args:
            entity_types: Lista de tipos de entidades a extraer.
                         Si es None, extrae todas.
                         Tipos disponibles en español: PER, ORG, LOC, MISC
        
        Returns:
            dict: Diccionario con tipo de entidad como clave y lista de entidades como valor
        """
        if self.document is None:
            raise ValueError("Primero debes cargar un documento con load_document()")
        
        # Limpiar el documento: reemplazar saltos de línea por espacios
        # para evitar que NER detecte entidades pegadas incorrectamente
        clean_document = ' '.join(self.document.split())
        
        # Procesar el documento limpio (no en minúsculas para mejor detección de NER)
        if self.doc is None or self.doc.text != clean_document:
            self.doc = self.nlp(clean_document)
        
        entities = {}
        
        for ent in self.doc.ents:
            # Filtrar por tipo si se especificó
            if entity_types is None or ent.label_ in entity_types:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
        
        # Complementar con regex para organizaciones que NER puede perder
        if entity_types is None or 'ORG' in entity_types:
            if 'ORG' not in entities:
                entities['ORG'] = []
            
            # Patrones comunes de organizaciones colombianas/internacionales
            import re
            org_patterns = [
                r'\b(Banco\s+(?:de\s+)?[\w\s]+?)(?:\s*-|\s*,|\s+[A-Z][a-z]+|\n)',
                r'\b(IBM|Microsoft|Oracle|Google|Amazon|Apple|Meta|Rappi|Globant|Bancolombia|Ecopetrol|Avianca)\b',
                r'\b(Universidad\s+[\w\s]+?de\s+Colombia)',
                r'\b(\w+\s+SAS)\b',
                r'\b(\w+\s+S\.?A\.?S?\.?)\b',
            ]
            
            for pattern in org_patterns:
                matches = re.finditer(pattern, clean_document, re.IGNORECASE)
                for match in matches:
                    org_name = match.group(1).strip()
                    if len(org_name) > 3:
                        entities['ORG'].append(org_name)
        
        return entities
    
    def get_entity_counts(self, entity_types=None):
        """
        Obtiene el conteo de cada entidad encontrada.
        
        Args:
            entity_types: Lista de tipos de entidades a contar
        
        Returns:
            dict: Diccionario con tipo de entidad y Counter de frecuencias
        """
        entities = self.extract_entities(entity_types)
        
        entity_counts = {}
        for entity_type, entity_list in entities.items():
            entity_counts[entity_type] = Counter(entity_list)
        
        return entity_counts
    
    def get_organizations(self, top_n=None):
        """
        Extrae solo organizaciones del texto.
        
        Args:
            top_n: Número de organizaciones más frecuentes a retornar
        
        Returns:
            Counter: Contador con organizaciones y sus frecuencias
        """
        entities = self.extract_entities(entity_types=['ORG'])
        orgs = Counter(entities.get('ORG', []))
        
        # Filtrar organizaciones falsas (cargos, palabras genéricas)
        cargos_palabras_falsas = {
            'líder', 'gerente', 'director', 'coordinador', 'analista',
            'desarrollador', 'ingeniero', 'cto', 'ceo', 'cio',
            'tech lead', 'software engineer', 'senior software engineer',
            'junior', 'solutions engineer', 'ciso', 'ejecutivo',
            'lider técnico', 'diferentes', 'ti', 'latam', 'emea',
            'applications lead', 'gerente pdm', 'coordinador de soporte',
            'ingeniero de operaciones', 'vicepresidente ejecutivo',
            'gerente técnico', 'gerente general', 'arquitecto de software',
            'ingeniero de software', 'cloud engineer', 'qa analyst',
            'lider', 'analista y programador', 'docente'
        }
        
        # Agregar stopwords personalizadas a la lista de filtrado
        cargos_palabras_falsas = cargos_palabras_falsas.union(self.custom_stopwords)
        
        # Filtrar y limpiar
        orgs_filtered = {}
        for org, count in orgs.items():
            # Limpiar espacios y saltos de línea
            clean_org = ' '.join(org.split())
            clean_lower = clean_org.lower()
            
            # Filtrar si la organización completa está en stopwords personalizadas
            if clean_lower in [sw.lower() for sw in self.custom_stopwords]:
                continue
            
            # Si es una palabra individual (sin espacios), verificar stopwords
            if ' ' not in clean_org:
                # Es palabra individual, aplicar filtro de stopwords
                if clean_lower in cargos_palabras_falsas or len(clean_org) <= 3:
                    continue
            
            # Si es frase completa, solo filtrar cargos conocidos
            if (clean_lower not in cargos_palabras_falsas and 
                len(clean_org) > 3 and
                not any(cargo in clean_lower for cargo in [
                    'ingeniero', 'desarrollador', 'analista', 'gerente',
                    'director', 'coordinador', 'líder', 'tech lead'
                ])):
                orgs_filtered[clean_org] = orgs_filtered.get(clean_org, 0) + count
        
        orgs_counter = Counter(orgs_filtered)
        
        if top_n:
            return dict(orgs_counter.most_common(top_n))
        return dict(orgs_counter)
    
    def get_persons(self, top_n=None):
        """
        Extrae solo personas del texto.
        
        Args:
            top_n: Número de personas más frecuentes a retornar
        
        Returns:
            Counter: Contador con personas y sus frecuencias
        """
        entities = self.extract_entities(entity_types=['PER'])
        persons = Counter(entities.get('PER', []))
        
        if top_n:
            return dict(persons.most_common(top_n))
        return dict(persons)
    
    def get_locations(self, top_n=None):
        """
        Extrae solo ubicaciones del texto.
        
        Args:
            top_n: Número de ubicaciones más frecuentes a retornar
        
        Returns:
            Counter: Contador con ubicaciones y sus frecuencias
        """
        entities = self.extract_entities(entity_types=['LOC'])
        locations = Counter(entities.get('LOC', []))
        
        if top_n:
            return dict(locations.most_common(top_n))
        return dict(locations)
    
    def print_entity_summary(self):
        """
        Imprime un resumen de todas las entidades encontradas.
        """
        entity_counts = self.get_entity_counts()
        
        print("\n" + "="*50)
        print("RESUMEN DE ENTIDADES NOMBRADAS (NER)")
        print("="*50 + "\n")
        
        entity_names = {
            'PER': 'Personas',
            'ORG': 'Organizaciones',
            'LOC': 'Ubicaciones',
            'MISC': 'Misceláneas'
        }
        
        for entity_type, counter in entity_counts.items():
            entity_name = entity_names.get(entity_type, entity_type)
            print(f"📍 {entity_name} ({entity_type}):")
            print(f"   Total encontradas: {len(counter)}")
            print(f"   Top 5:")
            for entity, count in counter.most_common(5):
                print(f"      • {entity}: {count} veces")
            print()
    
    def generate_wordcloud(self, width=800, height=400, background_color='white', **kwargs):
        """
        Genera la nube de palabras.
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            background_color: Color de fondo
            **kwargs: Otros argumentos para WordCloud
        
        Returns:
            WordCloud: Objeto WordCloud generado
        """
        # Si tenemos frecuencias de entidades, usar esas
        if self.entity_frequencies is not None:
            wordcloud = WordCloud(
                width=width, 
                height=height, 
                background_color=background_color,
                **kwargs
            ).generate_from_frequencies(self.entity_frequencies)
        # Si no, usar el texto filtrado tradicional
        elif self.filtered_text is not None:
            wordcloud = WordCloud(
                width=width, 
                height=height, 
                background_color=background_color,
                **kwargs
            ).generate(self.filtered_text)
        else:
            raise ValueError("Primero debes procesar el texto con process_text()")
        
        return wordcloud
    
    def generate_entity_wordcloud(self, entity_type='ORG', width=800, height=400, 
                                  background_color='white', **kwargs):
        """
        Genera una nube de palabras específica para un tipo de entidad.
        
        Args:
            entity_type: Tipo de entidad (ORG, PER, LOC, MISC)
            width: Ancho de la imagen
            height: Alto de la imagen
            background_color: Color de fondo
            **kwargs: Otros argumentos para WordCloud
        
        Returns:
            WordCloud: Objeto WordCloud generado
        """
        entity_counts = self.get_entity_counts(entity_types=[entity_type])
        
        if entity_type not in entity_counts or not entity_counts[entity_type]:
            raise ValueError(f"No se encontraron entidades del tipo {entity_type}")
        
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            **kwargs
        ).generate_from_frequencies(entity_counts[entity_type])
        
        return wordcloud
    
    def show_wordcloud(self, wordcloud=None, figsize=(10, 5)):
        """
        Muestra la nube de palabras en pantalla.
        
        Args:
            wordcloud: Objeto WordCloud (si es None, genera uno nuevo)
            figsize: Tamaño de la figura
        """
        if wordcloud is None:
            wordcloud = self.generate_wordcloud()
        
        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    
    def save_wordcloud(self, filename='nube_palabras.png', wordcloud=None, figsize=(10, 5)):
        """
        Guarda la nube de palabras en un archivo.
        
        Args:
            filename: Nombre del archivo de salida
            wordcloud: Objeto WordCloud (si es None, genera uno nuevo)
            figsize: Tamaño de la figura
        """
        if wordcloud is None:
            wordcloud = self.generate_wordcloud()
        
        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"✓ Nube de palabras guardada en: {filename}")


