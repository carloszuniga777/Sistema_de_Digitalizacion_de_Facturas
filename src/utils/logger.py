"""
Configuración centralizada del logger para todo el proyecto.

logging: Imprime en consola, similar a print() pero es para producción. Permite guardar los logs en un archivo.   

"""
import logging
from datetime import date


def configurar_logger():
    """
    Configura el logger una sola vez para todo el proyecto.
    Muestra mensajes en consola Y los guarda en un archivo .log
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),                                                     # ← consola
            logging.FileHandler(f"logs/facturas_{date.today()}.log", encoding="utf-8")   # ← archivo
        ]
    )