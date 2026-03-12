from google.genai import Client #SDK de Google Generative AI
from PIL import Image #Manipulación de imágen en Python.
import json #para convertir texto JSON en diccionarios Python
import os #Acceso a variables del SO para leer la API

# Inicializa el cliente. Si la variable de entorno GOOGLE_API_KEY está seteada, 
# la cogerá automáticamente.
client = Client(api_key=os.getenv("GOOGLE_API_KEY")) #obtiene la clave API almacenada en el entorno.
MODEL = "models/gemini-2.5-flash-image" #Definiciendo el modelo que se usara

def analizar_frigorifico(img: Image) -> dict:  #funcion que recibe una imagen tipo PIL y devuelve un diccionario y haciendo Prompt Engineering.
    prompt = """ 
        Eres un sistema de análisis de inventario de alimentos altamente preciso.
        Tu tarea es analizar la imagen proporcionada del interior de un frigorífico
        y extraer una lista estructurada en formato JSON puro.

        REGLAS:
        1. NO inventes datos. Si no puedes leer una marca claramente, devuelve null.
        2. Si hay un recipiente opaco, clasifícalo como "recipiente_desconocido".
        3. Para las cantidades, haz una estimación conservadora.
        4. Distingue entre ingredientes crudos y platos preparados.

        Añade un campo adicional "ingredientes_ingles" con los nombres de los ingredientes traducidos al inglés.

        ESTRUCTURA JSON:
        {
        "ingredientes_individuales": [
            {
            "nombre": "nombre genérico",
            "marca": "Marca si es legible, si no null",
            "cantidad_estimada": "ej. 1 cartón, 3 unidades",
            "estado_preparacion": "crudo, envasado, fresco"
            }
        ],
        "ingredientes_ingles": ["Nombre1 en inglés", "Nombre2 en inglés"],
        "platos_preparados_o_sobras": [
            {
            "descripcion": "ej. Tupperware de cristal con lentejas",
            "tipo_envase": "Tupperware plástico, olla, plato cubierto"
            }
        ],
        "elementos_no_identificables": "Número estimado de elementos no identificables"
        }

        Devuelve solo JSON, sin texto adicional ni markdown.
        """

    try:
        img = img.convert("RGB")

        # Sintaxis correcta para el nuevo SDK de Gemini
        respuesta = client.models.generate_content(
            model=MODEL,
            contents=[prompt, img] # Pasamos el prompt y la imagen directamente
        )

        # Extraer el texto generado es mucho más directo ahora
        texto_limpio = respuesta.text.strip()
        
        # 💡 TRUCO: A veces Gemini añade bloques markdown aunque le digas que no lo haga. 
        # Esto previene que json.loads() lance un error.
        if texto_limpio.startswith("```json"):
            texto_limpio = texto_limpio[7:-3].strip()
        elif texto_limpio.startswith("```"):
            texto_limpio = texto_limpio[3:-3].strip()

        # Parsear el texto a un diccionario de Python
        datos_frigorifico = json.loads(texto_limpio)
        return datos_frigorifico

    except Exception as e:
        print("Ocurrió un error al procesar la imagen:", e)
        return None

def obtener_ingredientes_ingles(resultado_analisis: dict) -> list:
    if resultado_analisis and "ingredientes_ingles" in resultado_analisis:
        return resultado_analisis["ingredientes_ingles"]
    return[]