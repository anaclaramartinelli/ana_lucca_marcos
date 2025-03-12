import pygame
import random
import time
import json

# Inicialização do Pygame
pygame.mixer.init()
pygame.init()

# Configurações da Tela
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jelly Jumble")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.Font('fonte.ttf', 30)

# Carregamento de Assets
background = pygame.image.load('imagens/Image nova.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_image1 = pygame.image.load('imagens/bob_esponja_com_rede.png').convert_alpha()
player_image2 = pygame.image.load('imagens/patrick_com_rede.png').convert_alpha()
agua_viva = pygame.image.load('imagens/AGUAVIVA.png').convert_alpha()
gary_image = pygame.image.load('imagens/gary.png').convert_alpha()
tubarao = pygame.image.load('imagens/holandes.png').convert_alpha()

# Sons
pygame.mixer.music.set_volume(0.4)
som_agua_viva = pygame.mixer.Sound('somag.mp3')
boom = pygame.mixer.Sound('boom.mp3')
som_gary = pygame.mixer.Sound('garysom.mp3')

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, image, keys):
        super().__init__()
        self.image = pygame.transform.scale(image, (80, 80))
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        self.speedx = 0
        self.speedy = 0
        self.keys = keys

    def update(self):
        keys = pygame.key.get_pressed()
        self.speedx = self.speedy = 0
        if keys[self.keys['up']]: self.speedy = -5
        if keys[self.keys['down']]: self.speedy = 5
        if keys[self.keys['left']]: self.speedx = -5
        if keys[self.keys['right']]: self.speedx = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rect.clamp_ip(window.get_rect())

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, width, height, speed_range=(2, 6)):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(random.randint(-100, -50), random.randint(0, HEIGHT - 100), width, height)
        self.speedx = random.randint(*speed_range)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.rect.x = -100
            self.rect.bottom = random.randint(0, HEIGHT - 100)

class GameManager:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.score1 = 0
        self.score2 = 0
        self.level = 0
        self.init_sprites()

    def init_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_aguas_vivas = pygame.sprite.Group()
        self.all_tubaroes = pygame.sprite.Group()
        self.all_gary = pygame.sprite.Group()

        self.player1 = Player(player_image1, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
        self.player2 = Player(player_image2, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})

        self.all_sprites.add(self.player1, self.player2)

        for _ in range(6):
            agua_viva = Obstacle(agua_viva, 60, 60)
            self.all_aguas_vivas.add(agua_viva)

        for _ in range(2):
            tubarao_obj = Obstacle(tubarao, 130, 90)
            self.all_tubaroes.add(tubarao_obj)

        self.gary = Obstacle(gary_image, 60, 60, speed_range=(6, 6))
        self.all_gary.add(self.gary)

    def handle_collisions(self):
        if pygame.sprite.spritecollide(self.player1, self.all_tubaroes, False):
            boom.play()
            self.player1.rect.center = (WIDTH / 3, HEIGHT - 8)
            self.score1 = 0

        if pygame.sprite.spritecollide(self.player2, self.all_tubaroes, False):
            boom.play()
            self.player2.rect.center = (WIDTH / 2, HEIGHT - 15)
            self.score2 = 0

        if pygame.sprite.spritecollide(self.player1, self.all_aguas_vivas, True):
            som_agua_viva.play()
            self.score1 += 1

        if pygame.sprite.spritecollide(self.player2, self.all_aguas_vivas, True):
            som_agua_viva.play()
            self.score2 += 1

        if pygame.sprite.spritecollide(self.player1, self.all_gary, True):
            som_gary.play()
            self.score1 += 4

        if pygame.sprite.spritecollide(self.player2, self.all_gary, True):
            som_gary.play()
            self.score2 += 4

    def draw(self):
        window.fill(PRETO)
        window.blit(background, (0, 0))
        self.all_tubaroes.draw(window)
        self.all_aguas_vivas.draw(window)
        self.all_gary.draw(window)
        self.all_sprites.draw(window)

        score1_text = fonte.render(f"Jogador 1: {self.score1}", True, BRANCO)
        window.blit(score1_text, (10, 10))
        score2_text = fonte.render(f"Jogador 2: {self.score2}", True, BRANCO)
        window.blit(score2_text, (10, 50))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update()
            self.handle_collisions()
            self.draw()

        pygame.quit()

# Executa o jogo
if __name__ == "__main__":
    GameManager().run()