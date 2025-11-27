import pygame
import sys
import time

pygame.init()

# --- Configuration écran ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Fenêtre borderless")

# --- Police ---
font_title = pygame.font.Font(None, 80)
font_context = pygame.font.Font(None, 50)

# --- Textes ---
welcome_text = "Bienvenue dans le jeu du professeur farfelu"
context_text = (
    "Un jour, le professeur farfelu de l’EPHEC a perdu la tête…\n"
    "Il a transformé tout le campus en un gigantesque plateau de jeu !\n\n"
    "Pour retrouver le parking et échapper à ses pièges farfelus,\n"
    "vous devrez affronter ses mini-jeux délirants.\n\n"
    "Préparez-vous à résoudre ses énigmes, éviter ses gadgets farfelus,\n"
    "et devenir le champion incontesté du laboratoire du professeur !\n\n"
    "Mais qui est donc ce professeur fou ???"
)

text_color = (255, 255, 255)
current_text_lines = [""]  # Liste pour chaque ligne
char_index = 0
line_index = 0
text_speed = 0.05  # secondes par lettre
last_update = time.time()

# --- Timer ---
start_time = time.time()
show_context = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((0, 0, 0))  # Fond noir

    # --- Déterminer quel texte afficher ---
    if not show_context and time.time() - start_time >= 5:
        show_context = True
        lines = context_text.split("\n")
        current_text_lines = [""] * len(lines)
        char_index = 0
        line_index = 0
        last_update = time.time()

    if not show_context:
        full_text = welcome_text
        font = font_title
        if char_index < len(full_text):
            if time.time() - last_update > text_speed:
                current_text_lines[0] += full_text[char_index]
                char_index += 1
                last_update = time.time()
        lines_to_display = current_text_lines
        font_to_use = font
    else:
        font = font_context
        # Animation ligne par ligne
        if line_index < len(lines):
            if char_index < len(lines[line_index]):
                if time.time() - last_update > text_speed:
                    current_text_lines[line_index] += lines[line_index][char_index]
                    char_index += 1
                    last_update = time.time()
            else:
                line_index += 1
                char_index = 0
        lines_to_display = current_text_lines
        font_to_use = font

    # --- Calcul pour centrer verticalement tout le bloc de texte ---
    total_height = sum([font_to_use.size(line)[1] for line in lines_to_display]) + (len(lines_to_display) - 1) * 5
    start_y = HEIGHT // 2 - total_height // 2

    # --- Affichage ---
    current_y = start_y
    for line in lines_to_display:
        text_surface = font_to_use.render(line, True, text_color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, current_y + text_surface.get_height() // 2))
        screen.blit(text_surface, text_rect)
        current_y += text_surface.get_height() + 5  # espacement entre lignes

    pygame.display.flip()
