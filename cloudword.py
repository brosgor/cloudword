from wordcloud import WordCloud
import spacy
import re

# nube de palabras
# extrae palabras de un texto usando spaCy para procesamiento de lenguaje natural en español

import matplotlib.pyplot as plt

# Cargar el modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# Agregar stopwords personalizados
custom_stopwords = {
    'puede', 'pueden', 'debe', 'deben', 'hace', 'hacen', 
    'dice', 'dicen', 'vez', 'veces', 'forma', 'manera',
    'través', 'ejemplo', 'casos', 'caso', 'tipo', 'tipos',
    'parte', 'partes', 'lugar', 'lugares', 'tiempo', 'momento',
    "programa","universidad","pregrado","carrera","problema"
}

# Agregar las stopwords personalizadas al modelo de spaCy
for word in custom_stopwords:
    nlp.vocab[word].is_stop = True

words = [
""
]

# Unir todos los textos en uno solo
text = " ".join(words)

# Procesar el texto con spaCy para obtener tokens lematizados y filtrados
doc = nlp(text.lower())

# Filtrar tokens: solo palabras (no puntuación), no stopwords, no espacios, longitud > 2
# y excluir palabras que no son sustantivos, adjetivos o verbos principales
#tener en cuenta los bigramas
filtered_words = []
for token in doc:
    if (not token.is_stop and  # No es stopword
        not token.is_punct and  # No es puntuación
        not token.is_space and  # No es espacio
        len(token.text) > 2 and  # Más de 2 caracteres
        token.pos_ in ['NOUN', 'ADJ', 'VERB'] and  # Solo sustantivos, adjetivos y verbos
        token.text.isalpha()):  # Solo letras (no números)
        filtered_words.append(token.lemma_)  # Usar la forma lematizada

filtered_text = " ".join(filtered_words)

# Generar la nube de palabras
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

# Mostrar la nube de palabras
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('nube_palabras.png')
