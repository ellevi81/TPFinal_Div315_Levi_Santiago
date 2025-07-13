# src/ui_functions.py (revisado y comentado)
import pygame
import settings

def create_button(x, y, width, height, text, image_path=None, color=settings.COLOR_GREY):
    """
    crea un diccionario que representa un boton.
    esto es muy util para mantener toda la informacion del boton en un solo lugar.
    """
    button_dict = {
        "rect": pygame.Rect(x, y, width, height),
        "text": text,
        "image": None, # por defecto no tiene imagen
        "color": color
    }
    # si se provee una ruta de imagen, la carga y la escala
    if image_path:
        image = pygame.image.load(image_path).convert_alpha()
        button_dict["image"] = pygame.transform.scale(image, (width, height))

    return button_dict

def draw_button(screen, button_dict, font=None, text_color=settings.COLOR_WHITE):
    """
    dibuja un boton en la pantalla a partir de su diccionario.
    """
    # si el boton tiene una imagen, la dibuja
    if button_dict["image"]:
        screen.blit(button_dict["image"], button_dict["rect"].topleft)
    # si no, dibuja un rectangulo con color
    else:
        pygame.draw.rect(screen, button_dict["color"], button_dict["rect"], border_radius=10)

    # si se especifica una fuente y el boton tiene texto, lo dibuja centrado
    if font and button_dict["text"]:
        text_surf = font.render(button_dict["text"], True, text_color)
        text_rect = text_surf.get_rect(center=button_dict["rect"].center)
        screen.blit(text_surf, text_rect)

def is_button_clicked(button_dict, event):
    """
    verifica si un boton fue clickeado.
    devuelve true si el evento es un click del mouse y la posicion del mouse
    esta dentro del rectangulo del boton.
    """
    # no se permite el uso de operadores ternarios en la cursada.
    # usamos un if/else completo para mayor claridad.
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_dict["rect"].collidepoint(event.pos): # collidepoint es clave para esto [cite: 1072]
            return True

    return False

def draw_text(screen, text, font, color, x, y, align="topleft"):
    """
    funcion helper para dibujar texto en la pantalla, con alineacion personalizable.
    """
    text_surf = font.render(str(text), True, color)

    # revisamos el parametro de alineacion para posicionar el texto
    if align == "center":
        # si es 'center', usamos (x, y) como el centro del texto
        text_rect = text_surf.get_rect(center=(x, y))
    elif align == "topright":
        # si es 'topright', usamos (x, y) como la esquina superior derecha
        text_rect = text_surf.get_rect(topright=(x, y))
    else: # por defecto, la alineacion es "topleft"
        # si es 'topleft', usamos (x, y) como la esquina superior izquierda
        text_rect = text_surf.get_rect(topleft=(x, y))

    screen.blit(text_surf, text_rect)