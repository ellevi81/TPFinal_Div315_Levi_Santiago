# src/settings.py (revisado y comentado)
# este archivo centraliza todas las constantes y configuraciones del juego.
# es una buena practica para mantener el codigo ordenado y facil de modificar.
# si queremos cambiar el ancho de la pantalla, solo lo hacemos aqui.

import os

# --- ui & display ---
WIDTH = 1280
HEIGHT = 720
FPS = 60

# --- colores (tuplas rgb) ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_ORANGE = (255, 140, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREY = (128, 128, 128)
COLOR_LIGHT_BLUE = (0,125,255)
COLOR_GREEN = (5,135,67)
COLOR_RED = (255, 0, 0)

# --- rutas a los archivos ---
# usamos os.path.join para que las rutas funcionen en cualquier sistema operativo
ASSETS_PATH = "assets"
FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
IMAGES_PATH = os.path.join(ASSETS_PATH, "images")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
DECK_IMAGES_PATH = os.path.join(IMAGES_PATH, "decks")
UI_PATH = os.path.join(IMAGES_PATH, "buttons_image")
DATA_PATH = "data"
RANKING_FILE = os.path.join(DATA_PATH, "ranking.json")
CONFIG_FILE = "configs.json"

# --- rutas de fondos de pantalla ---
BACKGROUND_PATH = os.path.join(IMAGES_PATH, "background_cards.png")
CARD_REVERSE_PATH = os.path.join(DECK_IMAGES_PATH, "blue_deck_expansion_1", "reverse.png")
DISCLAIMER_PATH = os.path.join(IMAGES_PATH, "agregados", "disclaimer.png")
MENU_BACKGROUND_PATH = os.path.join(IMAGES_PATH, "agregados", "menu.png")
SETTINGS_BACKGROUND_PATH = os.path.join(IMAGES_PATH, "forms", "img_3.jpg")
GAME_OVER_BACKGROUND_PATH = os.path.join(IMAGES_PATH, "agregados", "final2.png")
WISH_BACKGROUND_PATH = os.path.join(IMAGES_PATH, "agregados", "shenlong.png")

# --- rutas de iconos ---
ICON_SHIELD_PATH = os.path.join(IMAGES_PATH, "icons", "icon_shield.png")
ICON_HEAL_PATH = os.path.join(IMAGES_PATH, "icons", "icon_heal.png")
WISH_BUTTON_ICON_PATH = os.path.join(IMAGES_PATH, "icons", "7_star.png")
WISH_BUTTON_DISABLED_PATH = os.path.join(IMAGES_PATH, "agregados", "ALL_stars_disabled.png")

# --- rutas de musica ---
MUSIC_MENU = os.path.join(SOUNDS_PATH, "music", "torneo_menu.ogg")
MUSIC_SETTINGS = os.path.join(SOUNDS_PATH, "music", "sonido_prelude_dbz.ogg")
MUSIC_GAME_OVER = os.path.join(SOUNDS_PATH, "music", "ultra_instinct.ogg")
MUSIC_BATTLE = os.path.join(SOUNDS_PATH, "music", "batalla.ogg")
MUSIC_WISH = os.path.join(SOUNDS_PATH, "music", "form_wish_select.ogg")

# --- rutas de sonidos (efectos) ---
SOUND_WISH_INTRO = os.path.join(SOUNDS_PATH, "sounds", "wish_sound_intro.ogg")
SOUND_WISH_OUTRO = os.path.join(SOUNDS_PATH, "sounds", "wish_sound_outro.ogg")

# -- claves para diccionarios --
# usar constantes para las claves de los diccionarios evita errores de tipeo
KEY_CARD_ID = "id"
KEY_CARD_DECK = "deck"
KEY_CARD_STATS = "stats"
KEY_CARD_IMAGE = "image"
KEY_HP = "hp"
KEY_ATK = "atk"
KEY_DEF = "def"
KEY_STARS = "stars"

# -- estados del juego --
# usar constantes para los estados hace el codigo mas legible (en vez de usar numeros o strings)
STATE_DISCLAIMER = "disclaimer"
STATE_MAIN_MENU = "main_menu"
STATE_GAMEPLAY = "gameplay"
STATE_RANKING = "ranking"
STATE_SETTINGS = "settings"
STATE_GAME_OVER = "game_over"
STATE_WISH = "wish"

# --- posiciones y tamaños de la ui ---
PLAYER_STATS_POS = (125, 510)
ENEMY_STATS_POS = (125, 200)
PLAYER_DECK_POS = (400, 435)
PLAYER_CARD_POS = (680, 435)
ENEMY_DECK_POS = (400, 120)
ENEMY_CARD_POS = (680, 120)
TURN_RESULT_POS = (20, 20)
HEAL_BTN_POS = (1020, 480)
SHIELD_BTN_POS = (1020, 380)
PLAY_HAND_BTN_POS = (1000, 280)
WISH_BTN_POS = (1150, 600)
WISH_ICON_SIZE = (125, 125)
WISH_HEAL_BTN_POS = (WIDTH/4 - 64, 500)
WISH_SHIELD_BTN_POS = (WIDTH * 3/4 - 64, 500)
WISH_POWERUP_ICON_SIZE = (128, 128)