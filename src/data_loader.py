# src/data_loader.py (revisado y comentado)
import os
import json
import pygame
import settings

def parse_card_filename(filename, deck_name):
    """
    analiza el nombre de un archivo de imagen para extraer los datos de la carta.
    devuelve un diccionario con los datos o none si el nombre no es valido.
    es una forma inteligente de tener los datos sin escribirlos a mano.
    """
    # primera validacion: nos aseguramos de que sea un archivo .png y no el reverso
    if not filename.endswith('.png') or "reverse" in filename:
        return None

    # separamos el nombre del archivo por el caracter '_' para obtener las partes
    parts = filename.replace(".png", "").split('_')

    # validamos que el nombre tenga la estructura esperada (id, hp, atk, def, stars)
    if len(parts) < 8 or not (parts[1]=='HP' and parts[3]=='ATK' and parts[5]=='DEF'):
        return None
    if not (parts[2].isdigit() and parts[4].isdigit() and parts[6].isdigit() and parts[7].isdigit()):
        return None

    # verificamos que el archivo de imagen realmente exista en la carpeta
    path = os.path.join(settings.DECK_IMAGES_PATH, deck_name, filename)
    if not os.path.exists(path):
        return None

    # si todas las validaciones pasan, creamos el diccionario de la carta
    return {
        settings.KEY_CARD_ID: parts[0],
        settings.KEY_CARD_DECK: deck_name,
        # cargamos la imagen y la escalamos al tamaño deseado
        settings.KEY_CARD_IMAGE: pygame.transform.scale(pygame.image.load(path).convert_alpha(), (150, 220)),
        settings.KEY_CARD_STATS: {
            settings.KEY_HP: int(parts[2]),
            settings.KEY_ATK: int(parts[4]),
            settings.KEY_DEF: int(parts[6]),
            settings.KEY_STARS: int(parts[7])
        }
    }

def load_all_cards(deck_names):
    """
    recorre todas las carpetas de mazos y carga todas las cartas en un gran diccionario.
    la clave del diccionario es el nombre del mazo.
    """
    all_decks = {}
    for deck_name in deck_names:
        deck_path = os.path.join(settings.DECK_IMAGES_PATH, deck_name)
        if not os.path.isdir(deck_path):
            continue # si la carpeta no existe, la salteamos

        all_decks[deck_name] = []
        for filename in os.listdir(deck_path):
            card_data = parse_card_filename(filename, deck_name)
            if card_data:
                all_decks[deck_name].append(card_data)
    return all_decks

def load_json_file(file_path):
    """
    funcion generica para cargar un archivo json.
    devuelve el contenido del json como un diccionario o lista de python.
    """
    if not os.path.exists(file_path):
        return None # si el archivo no existe, no podemos cargarlo

    # usamos 'with' para asegurarnos de que el archivo se cierre correctamente
    with open(file_path, 'r') as f:
        content = f.read()

    # si el archivo no esta vacio, lo convertimos de json a diccionario/lista
    if content:
        return json.loads(content)

    return None # si el archivo esta vacio, devolvemos none

def save_ranking(ranking_list):
    """
    guarda la lista de ranking en un archivo json.
    el parametro indent=4 hace que el archivo sea facil de leer para una persona.
    """
    # si la carpeta 'data' no existe, la creamos
    if not os.path.exists(settings.DATA_PATH):
        os.makedirs(settings.DATA_PATH)

    with open(settings.RANKING_FILE, 'w') as f:
        json.dump(ranking_list, f, indent=4)