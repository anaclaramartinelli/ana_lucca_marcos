# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossy Ocean')

# ----- Inicia assets
largura = 80
altura = 80
larg_tub = 130
alt_tub = 90
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('imagens/fundo_mario.jpg').convert()

agua_viva = pygame.image.load('imagens/agua_viva.png').convert_alpha()
agua_viva_small = pygame.transform.scale(agua_viva, (largura, altura))

tubarao = pygame.image.load('imagens/shark03.png').convert_alpha()
tubarao_grande = pygame.transform.scale(tubarao, (larg_tub, alt_tub))

player_image = pygame.image.load('imagens/bob_esponja_direita.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (largura, altura))

# ----- Inicia estruturas de dados
game = True

class Player(pygame.sprite.Sprite):
    def __init__(self, imagens, keys):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imagens
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.keys = keys

    def update(self):
        # Atualização da posição do jogador
        keys = pygame.key.get_pressed()
        if keys[self.keys['up']]:
            self.speedy = -3
            self.speedx = 0
        elif keys[self.keys['down']]:
            self.speedy = 3
            self.speedx = 0
        else:
            self.speedy = 0

        if keys[self.keys['left']]:
            self.speedx = -3
            self.speedy = 0
        elif keys[self.keys['right']]:
            self.speedx = 3
            self.speedy = 0
        else:
            self.speedx = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantém dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

# ----- Criação dos jogadores
player1 = Player(player_image, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
player2 = Player(player_image, {'up': pygame.K_t, 'down': pygame.K_g, 'left': pygame.K_f, 'right': pygame.K_h})

class Peixe(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imgagens
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = random.randint(-100, -altura)
        self.speedx = 2
        self.speedy = 0

    def update(self):
        # Atualizando a posição do peixe
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o peixe passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = 0
            self.rect.y = random.randint(-100, HEIGHT - altura)
            self.speedx = random.randint(2, 4)
            self.speedy = 0

all_peixes = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Adiciona jogadores ao grupo de sprites
all_sprites.add(player1)
all_sprites.add(player2)

for i in range(6):
    peixe1 = Peixe(agua_viva_small)
    all_peixes.add(peixe1)

for i in range(4):
    tubarao = Peixe(tubarao_grande)
    all_peixes.add(tubarao)

clock = pygame.time.Clock()
FPS = 30

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    all_sprites.update()

    # Verifica colisão entre os jogadores e os obstáculos
    if pygame.sprite.spritecollide(player1, all_peixes, False) or pygame.sprite.spritecollide(player2, all_peixes, False):
        game = False

    for peixe in all_peixes:
        peixe.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (0, 0))

    all_peixes.draw(window)
    all_sprites.draw(window)

    pygame.display.update()

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados