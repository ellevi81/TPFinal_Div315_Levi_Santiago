# src/game_logic.py
import random #genera numero aleatorios y realiza selecciones aleatorias
import settings

def create_player_deck(all_cards_data, composition, total_cards):
    """
    crea un mazo aleatorio para un jugador a partir de un pool de cartas.
    'composition' indica cuantas copias de cada mazo se usan.
    'total_cards' es la cantidad de cartas que tendra el mazo final.
    """
    full_pool = []
    # recorremos la composicion definida en configs.json
    for deck_name, count in composition.items():
        if deck_name in all_cards_data:
            # agregamos las cartas de ese mazo, multiplicadas por su 'count'
            full_pool.extend(all_cards_data[deck_name] * count)

    # mezclamos todo el pool de cartas para que sea aleatorio
    random.shuffle(full_pool)

    # devolvemos solo la cantidad de cartas que necesitamos para el mazo
    return full_pool[:total_cards]

def calculate_initial_stats(deck):
    """
    calcula las estadisticas totales (hp, atk, def) de un jugador
    sumando los stats de todas las cartas de su mazo.
    """
    stats = {settings.KEY_HP: 0, settings.KEY_ATK: 0, settings.KEY_DEF: 0}
    for card in deck:
        stats[settings.KEY_HP] += card[settings.KEY_CARD_STATS][settings.KEY_HP]
        stats[settings.KEY_ATK] += card[settings.KEY_CARD_STATS][settings.KEY_ATK]
        stats[settings.KEY_DEF] += card[settings.KEY_CARD_STATS][settings.KEY_DEF]
    return stats

def get_bonus_multiplier(stars):
    """
    devuelve el multiplicador de bonus segun la cantidad de estrellas de la carta.
    usa un diccionario como si fuera un 'switch-case', es una tecnica muy comun.
    refactorizado para ser mas explicito y claro para un principiante.
    """
    # el enunciado pide un bonus especifico por estrella
    # nota: 'z' o 10 estrellas es lo mismo en el codigo, use 10 para que sea numerico
    bonus_map = {1: 1.01, 2: 1.02, 3: 1.03, 4: 1.04, 5: 1.05, 6: 1.06, 7: 1.07, 10: 1.10}

    # verificamos si la cantidad de estrellas tiene un bonus definido
    if stars in bonus_map:
        return bonus_map[stars]
    else:
        # si no tiene un bonus, el multiplicador es 1 (o sea, no hay bonus)
        return 1.0

def get_card_attack_with_bonus(card):
    """
    calcula el ataque de una carta aplicandole el bonus.
    se usa para comparar quien gana la mano.
    """
    stats = card[settings.KEY_CARD_STATS]
    multiplier = get_bonus_multiplier(stats[settings.KEY_STARS])
    return int(stats[settings.KEY_ATK] * multiplier)

def get_card_total_damage(card):
    """
    calcula el daño total (hp, atk, def) de una carta con el bonus aplicado.
    se usa para restar los stats al jugador que pierde la mano.
    """
    stats = card[settings.KEY_CARD_STATS]
    multiplier = get_bonus_multiplier(stats[settings.KEY_STARS])
    return {
        settings.KEY_HP: int(stats[settings.KEY_HP] * multiplier),
        settings.KEY_ATK: int(stats[settings.KEY_ATK] * multiplier),
        settings.KEY_DEF: int(stats[settings.KEY_DEF] * multiplier)
    }

def get_critical_hit_multiplier():
    """
    decide de forma aleatoria si un golpe es critico.
    devuelve un multiplicador de daño (1 para normal, 2 o 3 para critico).
    hay mas chances de que salga 1, para que los criticos sean especiales.
    """
    # esta lista define las probabilidades: 5/7 de golpe normal, 1/7 de x2, 1/7 de x3
    possible_multipliers = [1, 1, 1, 1, 1, 2, 3]

    # elegimos uno de los valores de la lista al azar
    multiplier = random.choice(possible_multipliers)

    return multiplier