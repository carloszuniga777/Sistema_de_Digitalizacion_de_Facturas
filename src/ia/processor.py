import os
import asyncio
from google import genai        # Geminis
from google.genai import types
from src.utils.prompts import prompt, instrucciones_sistema
from dotenv import load_dotenv  # Carga las variables de entorno

# Cargar variables de entorno desde el archivo .env
load_dotenv(".env")


# Envía el texto a Gemini y obtiene la respuesta estructurada en CSV,
# asegurando que solo devuelva datos válidos o 'error' en caso de problema.
GEMINIS_API_KEY = os.getenv("GOOGLE_GEMINIS_API_KEY")



"""
Envía el texto a OpenAI y obtiene la respuesta estructurada en CSV,
asegurando que solo devuelva datos válidos o 'error' en caso de problema.
"""

async def estructurar_texto(texto_no_estructurado_list: list[str], tamanio_lote=30)-> list[str]:

    texto_estructurado = []    

     # 1. Si la lista viene vacia se sale 
    if not texto_no_estructurado_list: 
        print('No se encontró ningun contenido para que la IA lo estructure')
        return texto_estructurado
 

    client = genai.Client(api_key=GEMINIS_API_KEY)                                                # Se inicializa Geminis
    semaforo = asyncio.Semaphore(3)                                                               # Máximo 3 llamadas simultáneas

    async def procesar_lote_geminis(lote, indice):
        async with semaforo:
            
            # Concatena todas las facturas separadas por el identificador
            separador = "\n\n--- FACTURA NUEVA ---\n\n"                                           # Se concatenan las facturas del lote en un solo string, separadas por una marca que permitirá al modelo identificar dónde termina una y empieza la siguiente.
            texto_lote = separador.join(lote)
            
            
            try:
                
                # Realizamos la petición a geminis 
                respuesta = await client.aio.models.generate_content(                              # Documentacion API: https://ai.google.dev/gemini-api/docs/quickstart?hl=es-419
                    model="gemini-3-flash-preview", 
                    contents=prompt + "\n Este es el texto a parsear:\n" + texto_lote,
                    config=types.GenerateContentConfig(
                        system_instruction=instrucciones_sistema,
                        temperature=0.1,                                                           # Baja temperatura para que sea más preciso y menos creativo
                    ),
                )

                return respuesta.text
            
            except asyncio.TimeoutError:
                print(f"Lote {indice}: Timeout, la API tardó demasiado.")
                return None

            except Exception as e:
                print(f"Error en lote {indice}: {e}")
                return None  

    
    # 2. Se crean TODAS las corrutinas primero (sin await), luego se resuelven juntas
    response = [ 
                procesar_lote_geminis(texto_no_estructurado_list[i:i + tamanio_lote], i)
               for i in range(0, len(texto_no_estructurado_list), tamanio_lote) 
             ]


    # 3. Se ejecutan todas las corrutinas de los lotes concurrentemente,
    # respetando el límite de 3 llamadas simultáneas impuesto por el semáforo.
    # Los resultados se recogen en el mismo orden de los lotes.
    contenido = await asyncio.gather(*response)

    print('Estructuración del contenido con IA finalizó')
     
    # 4. Solo devuelve una lista de elementos que fueron procesados correctamente, es decir, no son "None"   
    return [r for r in contenido if r is not None]  
