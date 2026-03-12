import json

#toma un archivo JSON generado por tu motor de recomendación y devolver directamente la lista de recetas que contiene, lista para usar en tu frontend.

def cargar_recomendaciones(json_file_path: str):
    """
    Carga el JSON generado por el motor de recomendación y devuelve la lista de recetas.
    """
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        return data.get("recipes", [])
    except Exception as e:
        print("Error al cargar JSON de recomendaciones:", e)
        return []