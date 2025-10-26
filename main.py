from cloudword import CloudWordAnalyzer

if __name__ == "__main__":
    analyzer = CloudWordAnalyzer()
    
    texto = """
        AQUI VA EL TEXTO DEL CUAL QUIERAS GENERAR LA NUBE DE PALABRAS
    """
    
    analyzer.load_document(text=texto)
    
    # ==================================================
    # CAMBIAR SOLO EL MODE AQUÍ
    # ==================================================
    
    # Nube de palabras tradicional
    # analyzer.process_text(mode='words')
    
    # Nube de organizaciones
    analyzer.process_text(mode='organizations')
    
    # Nube de personas
    # analyzer.process_text(mode='persons')
    
    # Nube de ubicaciones
    # analyzer.process_text(mode='locations')
    
    # ==================================================
    # Todo lo demás igual, no hay que cambiar nada más
    # ==================================================
    
    # Generar wordcloud más compacta para entidades
    wc = analyzer.generate_wordcloud(
        width=1600,
        height=800,
        background_color='white',
        colormap='tab20b',     # Tonos oscuros y opacos
        min_font_size=10,      # Tamaño mínimo de fuente
        max_font_size=150,     # Tamaño máximo para las más frecuentes
        #prefer_horizontal=0.8, # 80% horizontal
        collocations=False     # No combinar palabras
        
    )
    analyzer.save_wordcloud('nube_palabras.png', wordcloud=wc)

