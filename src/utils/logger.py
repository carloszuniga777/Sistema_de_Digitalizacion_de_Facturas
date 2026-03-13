"""
Configuración centralizada del logger para todo el proyecto.

logging: Imprime en consola, similar a print() pero es para producción. Permite guardar los logs en un archivo.   

"""

import logging
from logging.handlers import RotatingFileHandler

def configurar_logger():
    """
    Configura el logger una sola vez para todo el proyecto.
    Muestra mensajes en consola Y los guarda en un archivo .log
    """

    logger = logging.getLogger()                #  obtiene el logger raíz, todos los loggers del proyecto heredan de él

    #  Evita que si configurar_logger() se llama dos veces agregue handlers duplicados
    if logger.handlers:     
        return

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Consola
    console_handler = logging.StreamHandler()       #  imprime en la terminal
    console_handler.setFormatter(formatter)         

    # Escribe en archivo: Archivo rotativo
    file_handler = RotatingFileHandler(            
        "logs/facturas.log",
        maxBytes=5_000_000,                         # Cuando el archivo llega a 5MB lo rota automáticamente y crea uno nuevo, evitando que crezca infinitamente
        backupCount=3,                              # mantiene máximo 3 archivos de respaldo
        encoding="utf-8",
        delay=True                                  # no crea el archivo hasta que haya algo que escribir
    )
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)