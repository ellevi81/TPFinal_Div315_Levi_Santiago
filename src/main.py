# src/main.py
import pygame # nos da las herramientas para crear la ventana, dibujar imagenes, manejar sonido y eventos del mouse/teclado
import sys #nos da acceso a funciones del sistema. lo usamos para llamar a sys.exit() y cerrar el programa de forma segura
import os #permite interactuar con el sistema operativo. lo usamos para armar rutas de archivos con os.path.join() para que funcione en cualquier computadora
import settings #constantes. guardamos valores como el tamaño de la pantalla, colores y rutas a imagenes para tener mas orden en el codigo
import data_loader #carga y guardar datos, como leer el configs.json, el ranking, y procesar los archivos de las cartas
import game_logic #este tiene las reglas del juego: como se calcula el daño, quien gana, los bonus, etc. no dibuja nada, es solo la logica
import ui_functions #es la interfaz de usuario. tiene funciones para crear, dibujar y manejar los botones y el texto. ayuda a mantener main.py mas limpio

# --- funciones ayuda para sonido ---

def play_sfx(sound_asset, game_state):
    """
    reproduce un efecto de sonido solo si estan habilitados en la config.
    """
    if game_state['sfx_enabled']:
        sound_asset.play()

def play_music_for_screen(game_state):
    """
    carga y reproduce la musica correspondiente a la pantalla actual.
    detiene la musica anterior para que no se superpongan.
    """
    pygame.mixer.music.stop()
    if not game_state['music_enabled']:
        return # si la musica esta apagada, no hace nada

    # diccionario para mapear cada estado del juego con su cancion
    music_map = {
        settings.STATE_MAIN_MENU: settings.MUSIC_MENU,
        settings.STATE_SETTINGS: settings.MUSIC_SETTINGS,
        settings.STATE_GAME_OVER: settings.MUSIC_GAME_OVER,
        settings.STATE_WISH: settings.MUSIC_WISH,
        settings.STATE_GAMEPLAY: settings.MUSIC_BATTLE
    }
    music_file = music_map.get(game_state['current_screen'])

    # verifica si el archivo de musica existe antes de intentar cargarlo
    if music_file and os.path.exists(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1) # el -1 hace que la musica se repita en bucle
    elif music_file:
        # un pequeño aviso en consola si no encuentra el archivo, muy util para debuggear
        print("advertencia: no se encontro el archivo de musica: {0}".format(music_file))

def initialize_game_assets():
    """
    carga todos los assets (recursos) del juego una sola vez al inicio.
    esto es mucho mas eficiente que cargarlos en cada frame del bucle principal.
    devuelve un diccionario con todos los assets cargados.
    """
    assets = {}
    # --- fuentes ---
    assets['font_main'] = pygame.font.Font(os.path.join(settings.FONTS_PATH, "Saiyan-Sans.ttf"), 64)
    assets['font_medium'] = pygame.font.Font(os.path.join(settings.FONTS_PATH, "alagard.ttf"), 48)
    assets['font_small'] = pygame.font.Font(os.path.join(settings.FONTS_PATH, "alagard.ttf"), 28)

    # --- fondos ---
    assets['background_disclaimer'] = pygame.transform.scale(pygame.image.load(settings.DISCLAIMER_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['background_game'] = pygame.transform.scale(pygame.image.load(settings.BACKGROUND_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['background_menu'] = pygame.transform.scale(pygame.image.load(settings.MENU_BACKGROUND_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['background_settings'] = pygame.transform.scale(pygame.image.load(settings.SETTINGS_BACKGROUND_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['background_wish'] = pygame.transform.scale(pygame.image.load(settings.WISH_BACKGROUND_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['background_game_over'] = pygame.transform.scale(pygame.image.load(settings.GAME_OVER_BACKGROUND_PATH).convert(), (settings.WIDTH, settings.HEIGHT))
    assets['card_reverse_img'] = pygame.transform.scale(pygame.image.load(settings.CARD_REVERSE_PATH).convert_alpha(), (150, 220))

    # --- sonidos (sfx) ---
    assets['sound_win'] = pygame.mixer.Sound(os.path.join(settings.SOUNDS_PATH, "sounds", "critical_hit.ogg"))
    assets['sound_lose'] = pygame.mixer.Sound(os.path.join(settings.SOUNDS_PATH, "sounds", "hit_01.ogg"))
    assets['sound_click'] = pygame.mixer.Sound(os.path.join(settings.SOUNDS_PATH, "sounds", "menu_select.wav"))
    assets['sound_wish_intro'] = pygame.mixer.Sound(settings.SOUND_WISH_INTRO)
    assets['sound_wish_outro'] = pygame.mixer.Sound(settings.SOUND_WISH_OUTRO)

    # --- iconos ---
    assets['icon_shield'] = pygame.image.load(settings.ICON_SHIELD_PATH).convert_alpha()
    assets['icon_heal'] = pygame.image.load(settings.ICON_HEAL_PATH).convert_alpha()

    # --- botones ---
    # creamos todos los botones que son estaticos y los guardamos en un diccionario
    assets['buttons'] = {
        'start': ui_functions.create_button(settings.WIDTH/2 - 150, 280, 300, 80, "START", color=settings.COLOR_ORANGE),
        'ranking': ui_functions.create_button(settings.WIDTH/2 - 150, 380, 300, 80, "RANKING", color=settings.COLOR_LIGHT_BLUE),
        'settings': ui_functions.create_button(settings.WIDTH/2 - 150, 480, 300, 80, "OPCIONES", color=settings.COLOR_GREEN),
        'exit': ui_functions.create_button(settings.WIDTH/2 - 150, 580, 300, 80, "EXIT", color=settings.COLOR_GREY),
        'back': ui_functions.create_button(50, settings.HEIGHT - 100, 200, 60, "VOLVER", color=settings.COLOR_GREY),
        'play_hand': ui_functions.create_button(settings.PLAY_HAND_BTN_POS[0], settings.PLAY_HAND_BTN_POS[1], 250, 80, "", image_path=os.path.join(settings.UI_PATH, "btn_play_hand.png")),
        'heal': ui_functions.create_button(settings.HEAL_BTN_POS[0], settings.HEAL_BTN_POS[1], 200, 80, "", image_path=os.path.join(settings.UI_PATH, "heal.png")),
        'shield': ui_functions.create_button(settings.SHIELD_BTN_POS[0], settings.SHIELD_BTN_POS[1], 200, 80, "", image_path=os.path.join(settings.UI_PATH, "shield.png")),
        'wish': ui_functions.create_button(settings.WISH_BTN_POS[0], settings.WISH_BTN_POS[1], settings.WISH_ICON_SIZE[0], settings.WISH_ICON_SIZE[1], "", image_path=settings.WISH_BUTTON_ICON_PATH),
    }

    # cargamos la imagen  para el boton de deseo deshabilitado
    disabled_img_path = settings.WISH_BUTTON_DISABLED_PATH
    if os.path.exists(disabled_img_path):
        image = pygame.image.load(disabled_img_path).convert_alpha()
        assets['wish_disabled_img'] = pygame.transform.scale(image, settings.WISH_ICON_SIZE)
    else:
        # si por alguna razon no encuentra la imagen, crea un cuadrado gris, asi no creashea
        print(f"advertencia: no se encontro la imagen del boton deshabilitado en {disabled_img_path}")
        surface_gris = pygame.Surface(settings.WISH_ICON_SIZE)
        surface_gris.fill(settings.COLOR_GREY)
        assets['wish_disabled_img'] = surface_gris

    return assets

def reset_match_state(config, all_cards):
    """
    prepara un diccionario con el estado inicial para una nueva partida.
    esto hace que empezar un juego nuevo sea tan simple como llamar a esta funcion.
    """
    deck_comp = config["deck_composition"]
    cards_count = config["game_settings"]["cards_per_deck"]

    # creamos los mazos para el jugador y el enemigo
    player_deck = game_logic.create_player_deck(all_cards, deck_comp, cards_count)
    enemy_deck = game_logic.create_player_deck(all_cards, deck_comp, cards_count)

    # calculamos las estadisticas iniciales
    player_stats = game_logic.calculate_initial_stats(player_deck)
    enemy_stats = game_logic.calculate_initial_stats(enemy_deck)

    # con todas las variables listas, armamos el diccionario de la partida
    return {
        'player': {
            "deck": player_deck, "stats": player_stats,
            "initial_hp": player_stats[settings.KEY_HP], "score": 0,
            "shield_active": False,
            "heal_uses": config["game_settings"]["heal_uses"],
            "shield_uses": config["game_settings"]["shield_uses"]
        },
        'enemy': {"deck": enemy_deck, "stats": enemy_stats},
        'current_player_card': None, 'current_enemy_card': None,
        'turn_result': "",
        'crit_message': "",
        'game_timer': config["game_settings"]["initial_time_seconds"],
        'last_tick': pygame.time.get_ticks(), 'game_over_message': ""
    }

def handle_events(game_state, assets):
    """
    maneja todos los eventos del usuario (teclado, mouse) y actualiza el estado del juego.
    esta funcion es fundamental en el bucle principal
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state['running'] = False
            return

        current_screen = game_state['current_screen']

        # --- logica de eventos para cada pantalla ---

        if current_screen == settings.STATE_DISCLAIMER:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game_state['current_screen'] = settings.STATE_MAIN_MENU
                play_sfx(assets['sound_click'], game_state)
                play_music_for_screen(game_state)

        elif current_screen == settings.STATE_MAIN_MENU:
            if ui_functions.is_button_clicked(assets['buttons']['start'], event):
                game_state['current_screen'] = settings.STATE_GAMEPLAY
                game_state['match'] = reset_match_state(game_state['config'], game_state['all_cards'])
                game_state['wish_made'] = False # reiniciamos el deseo para la nueva partida
                game_state['wish_chosen'] = None
            elif ui_functions.is_button_clicked(assets['buttons']['ranking'], event):
                game_state['current_screen'] = settings.STATE_RANKING
            elif ui_functions.is_button_clicked(assets['buttons']['settings'], event):
                game_state['current_screen'] = settings.STATE_SETTINGS
            elif ui_functions.is_button_clicked(assets['buttons']['exit'], event):
                game_state['running'] = False

            # si cambiamos de pantalla, reproducimos sonido y musica
            if current_screen != game_state['current_screen']:
                play_sfx(assets['sound_click'], game_state)
                play_music_for_screen(game_state)

        elif current_screen == settings.STATE_SETTINGS:
            if ui_functions.is_button_clicked(assets['buttons']['back'], event):
                game_state['current_screen'] = settings.STATE_MAIN_MENU
                play_sfx(assets['sound_click'], game_state)
                play_music_for_screen(game_state)

            # logica para los botones de musica y sfx
            if ui_functions.is_button_clicked(game_state['btn_toggle_music'], event):
                game_state['music_enabled'] = not game_state['music_enabled']
                play_music_for_screen(game_state) # actualizamos la musica inmediatamente
            if ui_functions.is_button_clicked(game_state['btn_toggle_sfx'], event):
                game_state['sfx_enabled'] = not game_state['sfx_enabled']
                play_sfx(assets['sound_click'], game_state) # reproducimos un sonido para probar

        elif current_screen == settings.STATE_GAMEPLAY:
            match = game_state['match']
            if ui_functions.is_button_clicked(assets['buttons']['play_hand'], event):
                play_sfx(assets['sound_click'], game_state)
                play_hand(match, assets, game_state)

            # boton de deseo
            if not game_state['wish_made'] and ui_functions.is_button_clicked(assets['buttons']['wish'], event):
                game_state['wish_made'] = True
                game_state['current_screen'] = settings.STATE_WISH
                play_sfx(assets['sound_wish_intro'], game_state)
                play_music_for_screen(game_state)

            # botones de comodines (heal/shield)
            if game_state.get('wish_chosen') == 'heal' and match['player']['heal_uses'] > 0 and ui_functions.is_button_clicked(assets['buttons']['heal'], event):
                match['player']['stats'][settings.KEY_HP] = match['player']['initial_hp']
                match['player']['heal_uses'] = 0
                play_sfx(assets['sound_click'], game_state)

            if game_state.get('wish_chosen') == 'shield' and match['player']['shield_uses'] > 0 and ui_functions.is_button_clicked(assets['buttons']['shield'], event):
                match['player']['shield_active'] = True
                match['player']['shield_uses'] = 0
                play_sfx(assets['sound_click'], game_state)

        elif current_screen == settings.STATE_WISH:
            if ui_functions.is_button_clicked(assets['buttons']['wish_heal'], event):
                play_sfx(assets['sound_wish_outro'], game_state)
                game_state['wish_chosen'] = 'heal'
                game_state['current_screen'] = settings.STATE_GAMEPLAY
                play_music_for_screen(game_state)
            if ui_functions.is_button_clicked(assets['buttons']['wish_shield'], event):
                play_sfx(assets['sound_wish_outro'], game_state)
                game_state['wish_chosen'] = 'shield'
                game_state['current_screen'] = settings.STATE_GAMEPLAY
                play_music_for_screen(game_state)

        elif current_screen == settings.STATE_RANKING:
            if ui_functions.is_button_clicked(assets['buttons']['back'], event):
                game_state['current_screen'] = settings.STATE_MAIN_MENU
                play_sfx(assets['sound_click'], game_state)
                play_music_for_screen(game_state)

        elif current_screen == settings.STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                # evento para confirmar el nombre con enter
                if event.key == pygame.K_RETURN and game_state['player_name']:
                    new_entry = {"name": game_state['player_name'], "score": game_state['match']['player']['score']}
                    game_state['ranking'].append(new_entry)
                    # ordenamos el ranking de mayor a menor puntaje usando una funcion lambda como clave
                    game_state['ranking'].sort(key=lambda x: x['score'], reverse=True)
                    data_loader.save_ranking(game_state['ranking'][:10]) # guardamos solo el top 10
                    game_state['player_name'] = ""
                    game_state['current_screen'] = settings.STATE_MAIN_MENU
                    play_sfx(assets['sound_click'], game_state)
                    play_music_for_screen(game_state)
                # evento para borrar letras
                elif event.key == pygame.K_BACKSPACE:
                    game_state['player_name'] = game_state['player_name'][:-1]
                # evento para añadir letras y numeros
                elif len(game_state['player_name']) < 15 and event.unicode.isalnum():
                    game_state['player_name'] += event.unicode


def play_hand(match, assets, game_state):
    """
    ejecuta la logica de una mano. ahora separa el mensaje de turno y de critico.
    """
    if not match['player']["deck"] or not match['enemy']["deck"]:
        return

    config = game_state['config']

    # reiniciamos el mensaje de critico en cada mano
    match['crit_message'] = ""

    match['current_player_card'] = match['player']["deck"].pop(0)
    match['current_enemy_card'] = match['enemy']["deck"].pop(0)

    player_atk = game_logic.get_card_attack_with_bonus(match['current_player_card'])
    enemy_atk = game_logic.get_card_attack_with_bonus(match['current_enemy_card'])

    if player_atk > enemy_atk:
        play_sfx(assets['sound_win'], game_state)
        match['turn_result'] = "ganaste la mano!" # mensaje principal
        damage = game_logic.get_card_total_damage(match['current_enemy_card'])
        crit_multiplier = game_logic.get_critical_hit_multiplier()

        if crit_multiplier > 1:
            # si hay critico, ponemos el mensaje en su propia variable
            match['crit_message'] = "golpe critico x{0}!".format(crit_multiplier)

        for key in damage:
            match['enemy']["stats"][key] -= damage[key] * crit_multiplier
        match['player']['score'] += config['game_settings']['points_per_win'] * crit_multiplier

    elif enemy_atk > player_atk:
        if match['player']["shield_active"]:
            match['turn_result'] = "escudo activado!" # mensaje principal
            damage = game_logic.get_card_total_damage(match['current_enemy_card'])
            crit_multiplier = game_logic.get_critical_hit_multiplier()
            if crit_multiplier > 1:
                match['crit_message'] = "critico devuelto x{0}!".format(crit_multiplier)

            for key in damage:
                match['enemy']["stats"][key] -= damage[key] * crit_multiplier
            match['player']["shield_active"] = False
        else:
            play_sfx(assets['sound_lose'], game_state)
            match['turn_result'] = "perdiste la mano..." # mensaje principal
            damage = game_logic.get_card_total_damage(match['current_player_card'])
            crit_multiplier = game_logic.get_critical_hit_multiplier()

            if crit_multiplier > 1:
                match['crit_message'] = "golpe critico x{0}!".format(crit_multiplier)

            for key in damage:
                match['player']["stats"][key] -= damage[key] * crit_multiplier
    else:
        match['turn_result'] = "empate"

def update_game_state(game_state, assets):
    """
    actualiza el estado del juego que cambia con el tiempo, como el timer.
    tambien verifica las condiciones de fin de partida.
    """
    if game_state['current_screen'] != settings.STATE_GAMEPLAY:
        return

    match = game_state['match']

    # logica del temporizador
    if match['game_timer'] > 0:
        now = pygame.time.get_ticks()
        if now - match['last_tick'] > 1000: # ha pasado un segundo
            match['game_timer'] -= 1
            match['last_tick'] = now

    hp_player = match["player"]["stats"][settings.KEY_HP]
    hp_enemy = match["enemy"]["stats"][settings.KEY_HP]
    is_over = False

    # --- condiciones de fin de partida ---
    if hp_player <= 0 or (not match["player"]["deck"] and hp_player < hp_enemy):
        match['game_over_message'] = "derrota!"
        is_over = True
    elif hp_enemy <= 0 or (not match["enemy"]["deck"] and hp_enemy < hp_player):
        match['game_over_message'] = "victoria!"
        is_over = True
    elif match['game_timer'] <= 0:
        if hp_player > hp_enemy:
            match['game_over_message'] = "ganaste por tiempo!"
        else:
            match['game_over_message'] = "perdiste por tiempo"
        is_over = True

    if is_over:
        config = game_state['config']
        # si el jugador gano, calcula el bonus por tiempo
        if "victoria" in match['game_over_message'] or "ganaste" in match['game_over_message']:
            bonus = match['game_timer'] * config['game_settings']['bonus_points_time_factor']
            match['player']['score'] += bonus

        game_state['current_screen'] = settings.STATE_GAME_OVER
        play_music_for_screen(game_state)

def draw_screen(screen, game_state, assets):
    """
    funcion principal de dibujado. elige el fondo y los elementos correctos segun la pantalla.
    """
    current_screen = game_state['current_screen']
    backgrounds = {
        settings.STATE_DISCLAIMER: assets['background_disclaimer'],
        settings.STATE_MAIN_MENU: assets['background_menu'],
        settings.STATE_RANKING: assets['background_menu'],
        settings.STATE_SETTINGS: assets['background_settings'],
        settings.STATE_WISH: assets['background_wish'],
        settings.STATE_GAMEPLAY: assets['background_game'],
        settings.STATE_GAME_OVER: assets['background_game_over']
    }
    screen.blit(backgrounds.get(current_screen, assets['background_game']), (0, 0))

    # llama a la funcion de dibujado especifica para la pantalla actual
    if current_screen == settings.STATE_DISCLAIMER: _draw_disclaimer_screen(screen, assets)
    elif current_screen == settings.STATE_MAIN_MENU: _draw_main_menu(screen, assets)
    elif current_screen == settings.STATE_RANKING: _draw_ranking(screen, game_state, assets)
    elif current_screen == settings.STATE_GAMEPLAY: _draw_gameplay(screen, game_state, assets)
    elif current_screen == settings.STATE_SETTINGS: _draw_settings_screen(screen, game_state, assets)
    elif current_screen == settings.STATE_WISH: _draw_wish_screen(screen, assets)
    elif current_screen == settings.STATE_GAME_OVER: _draw_game_over_screen(screen, game_state, assets)

def _draw_disclaimer_screen(screen, assets):
    """
    dibuja la pantalla inicial de disclaimer.
    """
    ui_functions.draw_text(screen, "presione cualquier tecla para continuar...", assets['font_small'], settings.COLOR_YELLOW, settings.WIDTH / 2, settings.HEIGHT - 40, align="center")

def _draw_game_over_screen(screen, game_state, assets):
    """
    dibuja la pantalla de fin de partida con el cuadro para ingresar nombre.
    """
    match = game_state['match']

    # dibuja el mensaje de victoria o derrota
    ui_functions.draw_text(screen, match['game_over_message'], assets['font_main'], settings.COLOR_YELLOW, settings.WIDTH / 2, 150, align="center")

    # dibuja el puntaje final
    score_text = "puntaje final: {0}".format(match['player']['score'])
    ui_functions.draw_text(screen, score_text, assets['font_medium'], settings.COLOR_WHITE, settings.WIDTH / 2, 250, align="center")

    # dibuja el cuadro de texto para el nombre
    ui_functions.draw_text(screen, "ingresa tu nombre:", assets['font_medium'], settings.COLOR_WHITE, settings.WIDTH / 2, 350, align="center")
    input_rect = pygame.Rect(settings.WIDTH / 2 - 200, 400, 400, 60)
    pygame.draw.rect(screen, settings.COLOR_GREY, input_rect, border_radius=10)
    pygame.draw.rect(screen, settings.COLOR_LIGHT_BLUE, input_rect, 3, border_radius=10)

    # dibuja el nombre que el usuario esta tipeando
    name_text_surface = assets['font_medium'].render(game_state['player_name'], True, settings.COLOR_WHITE)
    name_rect = name_text_surface.get_rect(midleft=(input_rect.x + 15, input_rect.centery))
    screen.blit(name_text_surface, name_rect)

def _draw_settings_screen(screen, game_state, assets):
    """
    dibuja la pantalla de configuracion.
    """
    ui_functions.draw_text(screen, "opciones", assets['font_main'], settings.COLOR_YELLOW, settings.WIDTH/2, 100, align="center")

    # definimos el texto y color del boton de musica segun su estado
    if game_state['music_enabled']:
        music_text = "musica: on"
        music_color = settings.COLOR_GREEN
    else:
        music_text = "musica: off"
        music_color = settings.COLOR_RED

    # definimos el texto y color del boton de sfx segun su estado
    if game_state['sfx_enabled']:
        sfx_text = "sonidos: on"
        sfx_color = settings.COLOR_GREEN
    else:
        sfx_text = "sonidos: off"
        sfx_color = settings.COLOR_RED

    # creamos los botones dinamicamente para que el texto y color se actualicen
    game_state['btn_toggle_music'] = ui_functions.create_button(settings.WIDTH/2 - 150, 250, 300, 80, music_text, color=music_color)
    game_state['btn_toggle_sfx'] = ui_functions.create_button(settings.WIDTH/2 - 150, 350, 300, 80, sfx_text, color=sfx_color)

    # dibujamos los botones
    ui_functions.draw_button(screen, game_state['btn_toggle_music'], assets['font_medium'])
    ui_functions.draw_button(screen, game_state['btn_toggle_sfx'], assets['font_medium'])
    ui_functions.draw_button(screen, assets['buttons']['back'], assets['font_medium'])

def _draw_main_menu(screen, assets):
    """
    dibuja la pantalla del menu principal.
    """
    ui_functions.draw_text(screen, "dragon ball tcg", assets['font_main'], settings.COLOR_ORANGE, settings.WIDTH / 2, 150, align="center")
    for btn_name in ['start', 'ranking', 'settings', 'exit']:
        ui_functions.draw_button(screen, assets['buttons'][btn_name], assets['font_medium'])

def _draw_ranking(screen, game_state, assets):
    """
    dibuja la pantalla de ranking.
    """
    ui_functions.draw_text(screen, "ranking", assets['font_main'], settings.COLOR_YELLOW, settings.WIDTH / 2, 100, align="center")
    # recorremos la lista del ranking y dibujamos cada entrada
    for i, entry in enumerate(game_state['ranking']):
        text = "{0}. {1}: {2}".format(i + 1, entry['name'], entry['score'])
        ui_functions.draw_text(screen, text, assets['font_medium'], settings.COLOR_WHITE, settings.WIDTH / 2, 200 + i * 50, align="center")
    ui_functions.draw_button(screen, assets['buttons']['back'], assets['font_medium'])

def _draw_gameplay(screen, game_state, assets):
    """
    dibuja todos los elementos de la pantalla de juego.
    """
    match = game_state['match']
    # dibujamos stats, cartas, etc.
    ui_functions.draw_text(screen, "hp: {0}".format(max(0, match['player']['stats'][settings.KEY_HP])), assets['font_small'], settings.COLOR_WHITE, settings.PLAYER_STATS_POS[0], settings.PLAYER_STATS_POS[1])
    ui_functions.draw_text(screen, "score: {0}".format(match['player']['score']), assets['font_small'], settings.COLOR_YELLOW, settings.PLAYER_STATS_POS[0], settings.PLAYER_STATS_POS[1] + 30)
    ui_functions.draw_text(screen, "hp: {0}".format(max(0, match['enemy']['stats'][settings.KEY_HP])), assets['font_small'], settings.COLOR_WHITE, settings.ENEMY_STATS_POS[0], settings.ENEMY_STATS_POS[1])

    ui_functions.draw_text(screen, "tiempo: {0}".format(match['game_timer']), assets['font_medium'], settings.COLOR_ORANGE, settings.WIDTH/2, 50, align="center")

    screen.blit(assets['card_reverse_img'], settings.ENEMY_DECK_POS)
    ui_functions.draw_text(screen, "cartas: {0}".format(len(match['enemy']['deck'])), assets['font_small'], settings.COLOR_WHITE, settings.ENEMY_DECK_POS[0] + 30, settings.ENEMY_DECK_POS[1] + 230)
    screen.blit(assets['card_reverse_img'], settings.PLAYER_DECK_POS)
    ui_functions.draw_text(screen, "cartas: {0}".format(len(match['player']['deck'])), assets['font_small'], settings.COLOR_WHITE, settings.PLAYER_DECK_POS[0] + 30, settings.PLAYER_DECK_POS[1] + 230)
    if match['current_enemy_card']: screen.blit(match['current_enemy_card'][settings.KEY_CARD_IMAGE], settings.ENEMY_CARD_POS)
    if match['current_player_card']: screen.blit(match['current_player_card'][settings.KEY_CARD_IMAGE], settings.PLAYER_CARD_POS)
    ui_functions.draw_button(screen, assets['buttons']['play_hand'])

    # logica para dibujar el boton de deseo segun su estado
    if not game_state['wish_made']:
        # si el deseo no se pidio, el boton es clickeable
        ui_functions.draw_button(screen, assets['buttons']['wish'])
    else:
        # si el deseo ya se uso, dibujamos la imagen deshabilitada
        screen.blit(assets['wish_disabled_img'], settings.WISH_BTN_POS)
    
    if game_state.get('wish_chosen') == 'heal' and match["player"]["heal_uses"] > 0: ui_functions.draw_button(screen, assets['buttons']['heal'])
    if game_state.get('wish_chosen') == 'shield' and match["player"]["shield_uses"] > 0: ui_functions.draw_button(screen, assets['buttons']['shield'])

    ui_functions.draw_text(screen, match['turn_result'], assets['font_medium'], settings.COLOR_YELLOW, settings.TURN_RESULT_POS[0], settings.TURN_RESULT_POS[1], align="topleft")

    if match['crit_message']:
        ui_functions.draw_text(screen, match['crit_message'], assets['font_medium'], settings.COLOR_RED, settings.WIDTH - 20, 20, align="topright")

def _draw_wish_screen(screen, assets):
    """
    dibuja la pantalla para elegir un deseo.
    """
    ui_functions.draw_text(screen, "pide un deseo...", assets['font_main'], settings.COLOR_YELLOW, settings.WIDTH / 2, 100, align="center")

    # creamos y dibujamos los botones de los deseos
    assets['buttons']['wish_heal'] = ui_functions.create_button(settings.WISH_HEAL_BTN_POS[0], settings.WISH_HEAL_BTN_POS[1], settings.WISH_POWERUP_ICON_SIZE[0], settings.WISH_POWERUP_ICON_SIZE[1], "", image_path=settings.ICON_HEAL_PATH)
    assets['buttons']['wish_shield'] = ui_functions.create_button(settings.WISH_SHIELD_BTN_POS[0], settings.WISH_SHIELD_BTN_POS[1], settings.WISH_POWERUP_ICON_SIZE[0], settings.WISH_POWERUP_ICON_SIZE[1], "", image_path=settings.ICON_SHIELD_PATH)

    ui_functions.draw_button(screen, assets['buttons']['wish_heal'])
    ui_functions.draw_button(screen, assets['buttons']['wish_shield'])

def main():
    """
    funcion principal que inicia y corre el juego. aqui empieza todo.
    """
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Dragon Ball Z TCG")
    clock = pygame.time.Clock()

    # cargamos la configuracion y los datos iniciales
    config = data_loader.load_json_file(settings.CONFIG_FILE)
    if not config:
        print("error: no se pudo cargar el archivo de configuracion.")
        return

    deck_names = list(config.get("deck_composition", {}).keys())
    all_cards = data_loader.load_all_cards(deck_names)
    ranking_data = data_loader.load_json_file(settings.RANKING_FILE)
    if ranking_data is None:
        ranking_data = []

    # cargamos todos los recursos (imagenes, fuentes, sonidos)
    assets = initialize_game_assets()

    # creamos el diccionario principal que contendra todo el estado del juego
    game_state = {
        'running': True, 'current_screen': settings.STATE_DISCLAIMER,
        'config': config, 'all_cards': all_cards, 'ranking': ranking_data,
        'player_name': "", 'match': None, 'music_enabled': True, 'sfx_enabled': True,
        'btn_toggle_music': None, 'btn_toggle_sfx': None,
        'wish_made': False,
        'wish_chosen': None
    }

    # --- el bucle principal del juego (game loop) ---
    while game_state['running']:
        clock.tick(settings.FPS) # controlamos la velocidad del juego

        # 1. manejamos los eventos del usuario
        handle_events(game_state, assets)

        # 2. actualizamos el estado del juego
        update_game_state(game_state, assets)

        # 3. dibujamos todo en la pantalla
        draw_screen(screen, game_state, assets)

        # 4. actualizamos la pantalla para que se vean los cambios
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()