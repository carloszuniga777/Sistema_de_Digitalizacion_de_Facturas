import requests
import os
from dotenv import load_dotenv
import logging  


load_dotenv()                           # Carga las variables de entorno

logger = logging.getLogger(__name__)    # ← __name__ toma el nombre del módulo automáticamente




BCH_API_KEY = os.getenv("BCH_API_KEY")
BCH_URL     = "https://bchapi-am.azure-api.net/api/v1/indicadores/97/cifras?reciente=1&formato=json"

def obtener_tasa_cambio() -> float | None:
    try:
        # Peticion    
        response = requests.get(
            BCH_URL,
            headers={"clave": BCH_API_KEY},
            timeout=10
        )
        
     
        response.raise_for_status()             # Lanza una excepción automáticamente si el servidor devuelve un código de error HTTP como 400, 401, 403, 404, 500
        data = response.json()
        tasa = float(data[0]["Valor"])
        
        return tasa
    except Exception as e:
        logger.error(f"Error al obtener tasa de cambio: {e}")
        return None

if __name__ == "__main__":
    tasa = obtener_tasa_cambio()
    print(tasa)