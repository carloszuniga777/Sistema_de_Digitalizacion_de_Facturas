import re

def limpiar_texto_ocr(texto: str) -> str:
    
    # Corrige RTN mal leído por OCR. Ej: BTN: → RTN:
    texto = re.sub(r'\b[A-Z0-9]TN:', 'RTN:', texto)
    
    # Corrige número de factura con letras mezcladas (007-00l-0l → 007-001-01)
    texto = re.sub(r'\b(\d{3}-\d{2})[lI](-\d{2})[lI]', r'\g<1>1\g<2>1', texto)
    

    # Une etiquetas de total separadas de su valor por salto de línea. 
    #  - Cubre: TOTAL, TOTAL A PAGAR, TOTAL FINAL, GRAND TOTAL, IMPORTE TOTAL, etc.
    #  - Cubre: L. 23,373.75 / L16,737.00 / L 23,373.75
    # Ej: "Total a pagar:\nL. 23,373.75" → "Total a pagar: L. 23,373.75"
    texto = re.sub(r'(?i)(total[^\n]*:)\s*\n\s*(L[\.\s]?\d)', r'\1 \2', texto)

    return texto