import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import logging  


load_dotenv()                           # Carga las variables de entorno
logger = logging.getLogger(__name__)    # Configuracion de logger 

# API BANCO CENTRAL DE HONDURAS: https://bchapi-am.developer.azure-api.net/
BCH_API_KEY = [ os.getenv("BCH_API_KEY_1"), os.getenv("BCH_API_KEY_2") ]
BCH_API     = "https://bchapi-am.azure-api.net/api/v1/indicadores/97/cifras?reciente=1&formato=json"



# API EUROPEAN CENTRAL BANK: https://data.ecb.europa.eu/help/api/data
ECB_API = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=1&format=jsondata"



# Ubicacion del archivo de cache de tasa de cambio
CACHE_DOLAR = Path(__file__).parent.parent / "cache" / "tasa_cambio_dolar.json"
CACHE_EURO = Path(__file__).parent.parent / "cache" / "tasa_cambio_euro.json"


#--- Funciones privdadas para guardar y leer cache --------

def _leer_cache(cache_file: Path, moneda: str) -> float | None:
    if cache_file.exists():
        tasa_cache = json.loads(cache_file.read_text())["tasa"]
        logger.warning(f"⚠️ Usando tasa en caché: {moneda}. {tasa_cache}")
        return tasa_cache
    
    logger.error("❌ No hay caché disponible, no se pudo obtener la tasa")
    return None


def _guardar_cache(cache_file: Path, tasa: float):
    cache_file.write_text(json.dumps({"tasa": tasa}))

#---------------------------------


# Obteniendo la tasa de cambio de dolar del Banco Central de Honduras
def obtener_tasa_cambio_dolar() -> float | None:
        for api_key in BCH_API_KEY:
            try:
                # Peticion    
                response = requests.get(
                    BCH_API,
                    headers={"clave": api_key},
                    timeout=10
                )
                
            
                response.raise_for_status()             # Lanza una excepción automáticamente si el servidor devuelve un código de error HTTP como 400, 401, 403, 404, 500
                data = response.json()                  # Convierte a JSON
                tasa = float(data[0]["Valor"])          # Obtiene el valor de la tasa
                
                # Guardar en caché en formato json
                _guardar_cache(CACHE_DOLAR, tasa)

                logger.info(f"✅ Tasa de cambio USD/L obtenida del BCH: L. {tasa}")
                
                return tasa
            
            except Exception as e:
                logger.warning(f"⚠️ API key fallida, intentando siguiente: {e}")
                continue
        
        # Si ambas API keys fallaron
        logger.warning("⚠️ Ambas API del BCH fallaron, usando caché")
        return _leer_cache(CACHE_DOLAR, "L")                                       # Lee la tasa almacenada en cache     



# Obteniendo la tasa de cambio euros a dolares del European Central Bank
def obtener_tasa_cambio_euro() -> float | None:
    try:
        response = requests.get(ECB_API, timeout=10)                                        # Peticion
        
        response.raise_for_status()                                                         # Lanza una excepción automáticamente si el servidor devuelve un código de error HTTP como 400, 401, 403, 404, 500
        data = response.json()                                                              # Convierte a JSON          
        tasa = float(data["dataSets"][0]["series"]["0:0:0:0:0"]["observations"]["0"][0])    # Obtiene el valor de la tasa
        
        # Guardar en caché en formato json
        _guardar_cache(CACHE_EURO, tasa)                            
        
        logger.info(f"✅ Tasa EUR/USD obtenida del ECB: {tasa}")
        
        return tasa
    
    except Exception as e:
        logger.warning(f"⚠️ API ECB no disponible: {e}")
        return _leer_cache(CACHE_EURO, "USD")                                                  # Lee la tasa almacenada en cache 

