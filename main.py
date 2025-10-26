from cloudword import CloudWordAnalyzer
# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del analizador
    analyzer = CloudWordAnalyzer()
    
    # Cargar documento desde CSV
    # analyzer.load_document(database='estudiantes.csv', 
    #                       column='Justifique la respuesta anterior (¿Por qué ?)')
    
    # O cargar texto directo

    analyzer.load_document(text="")
    
    # Procesar el texto
    analyzer.process_text()
    
    # Generar y guardar la nube de palabras
    analyzer.save_wordcloud('nube_palabras.png')
