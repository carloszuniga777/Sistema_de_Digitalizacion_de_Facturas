import os
import logging   # Imprime print() en produccion 

logger = logging.getLogger(__name__)  # ← __name__ toma el nombre del módulo automáticamente


def obtener_facturas() -> list[str]:
    facturas = []
    carpeta_factura = "./facturas"
    contenido = os.listdir(carpeta_factura)

    if not contenido:
        logger.warning("❌ La carpeta 'facturas' está vacía. No hay nada que procesar.")
        return []
             

    # Recorrer todas las carpetas dentro de la carpeta "facturas"
    for carpeta in sorted(os.listdir(carpeta_factura)):
        ruta_carpeta_meses = os.path.join(carpeta_factura + "/", carpeta)

        # Verificar que sea una carpeta antes de intentar listar
        if not os.path.isdir(ruta_carpeta_meses):
            logger.warning(f"⚠️ Ignorando archivo suelto: {ruta_carpeta_meses}")
            continue

        # Recorrer todos los archivos dentro de la carpeta
        for archivo in os.listdir(ruta_carpeta_meses):
            ruta_pdf = os.path.join(ruta_carpeta_meses + "/", archivo)

            facturas.append(ruta_pdf)

    
    logger.info('✅ Finalizo la extracción de las rutas de los archivos')

    return facturas
