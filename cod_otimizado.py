# ----- Importa e inicia pacotes
import pygame
import random
from configuracoes import WIDTH, HEIGHT
from game_screen import game_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossy Ocean')

game_screen(window)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados