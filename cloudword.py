from wordcloud import WordCloud
import spacy
import pandas as pd
import matplotlib.pyplot as plt


class CloudWordAnalyzer:
    """
    Clase para analizar texto y generar nubes de palabras usando spaCy y WordCloud.
    """
    
    def __init__(self, model='es_core_news_sm', custom_stopwords=None):
        """
        Inicializa el analizador con el modelo de spaCy y stopwords personalizados.
        
        Args:
            model: Nombre del modelo de spaCy a cargar
            custom_stopwords: Set de palabras a excluir del análisis
        """
        self.nlp = spacy.load(model)
        self.custom_stopwords = custom_stopwords or {
            'puede', 'pueden', 'debe', 'deben', 'hace', 'hacen', 
            'dice', 'dicen', 'vez', 'veces', 'forma', 'manera',
            'través', 'ejemplo', 'casos', 'caso', 'tipo', 'tipos',
            'parte', 'partes', 'lugar', 'lugares', 'tiempo', 'momento',
            'programa', 'universidad', 'pregrado', 'carrera', 'problema', 
            'estudiante', 'universitario', 'el', 'él', 'necesario', 
            'permitir', 'engineer', 'developer', 'empresa', 'sa', 'docente'
        }
        self._add_custom_stopwords()
        self.document = None
        self.filtered_text = None
        
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
    
    def process_text(self, pos_filter=None):
        """
        Procesa el texto con spaCy, aplicando filtros y lematización.
        
        Args:
            pos_filter: Lista de POS tags a mantener (default: NOUN, ADJ, VERB)
        
        Returns:
            str: Texto filtrado y procesado
        """
        if self.document is None:
            raise ValueError("Primero debes cargar un documento con load_document()")
        
        if pos_filter is None:
            pos_filter = ['NOUN', 'ADJ', 'VERB']
        
        doc = self.nlp(self.document.lower())
        
        filtered_words = []
        for token in doc:
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
        return self.filtered_text
    
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
        if self.filtered_text is None:
            raise ValueError("Primero debes procesar el texto con process_text()")
        
        wordcloud = WordCloud(
            width=width, 
            height=height, 
            background_color=background_color,
            **kwargs
        ).generate(self.filtered_text)
        
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
        plt.savefig(filename)
        plt.close()
        print(f"✓ Nube de palabras guardada en: {filename}")


