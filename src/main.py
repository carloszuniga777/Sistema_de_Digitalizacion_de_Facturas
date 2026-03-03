import os

# Desactiva verificación de red
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"   # Desactiva la verificación de conectividad al inicio 
                                                               # (un chequeo de red que no es necesario para usar el OCR Paddleocr). 
                                                               # El reconocimiento de texto sigue funcionando igual.         

from src.ocr.extractor          import InvoiceOCRExtractor
from src.utils.file_manager     import obtener_facturas
from src.utils.data_transformer import csv_a_dataframe
from src.ia.processor           import estructurar_texto
from src.database.repository    import cargar_sql
import asyncio
import nest_asyncio
nest_asyncio.apply()  # Necesario para ejecutar asyncio en Positron/Jupyter/IPython


async def main():
    
    # 1. Inicializa el extractor de pdf e imagenes
    extractor = InvoiceOCRExtractor()              

    # 2. Obtiene las rutas de las facturas 
    ruta_archivos = obtener_facturas()
        
    # 3. Extrae el contenido de los pdf  
    texto_pdf = extractor.extraer_texto_pdf(ruta_archivos)
     
    # 4. Extrae el contenido de las imagenes
    texto_img = extractor.extraer_texto_imagenes(ruta_archivos)

    # 5. Unifica lista pdf e imagenes en una sola lista
    texto_no_extructurado = texto_pdf + texto_img    

    # 6. Extructura el contenido en formato cvs 
    texto_estructurado = await estructurar_texto(texto_no_extructurado)

     # 7. Lo convierte a dataframe
    df = csv_a_dataframe(texto_estructurado)

    # 8. Lo carga a la base de datos
    cargar_sql(df)

    return df, texto_no_extructurado, texto_estructurado

if __name__ == "__main__":
    df, texto_no_extructurado, texto_estructurado = asyncio.run(main())