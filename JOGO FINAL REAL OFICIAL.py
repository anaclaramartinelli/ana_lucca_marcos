import pygame
import random
import time
import json


pygame.mixer.init()
pygame.init()


# ----- Inicia assets e constantes
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255,0,0)
CINZA = (117, 120, 123)

largura_agua_viva = 60
altura_agua_viva = 60
largura_player = 80
altura_player = 80
largura_hol = 130
level = 0
altura_hol = 90

player_name = ""

fonte = pygame.font.Font('fonte.ttf', 30)

background = pygame.image.load('imagens/Image nova.jpg').convert()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

Tela_tutorial = pygame.image.load('tela_instrucoes.png').convert()
Tela_tutorial = pygame.transform.scale(Tela_tutorial,(WIDTH,HEIGHT))

agua_viva = pygame.image.load('imagens/AGUAVIVA.png').convert_alpha()
agua_viva_small = pygame.transform.scale(agua_viva, (largura_agua_viva, altura_agua_viva))

holandes = pygame.image.load('imagens/holandes.png').convert_alpha()
hoandes_grande = pygame.transform.scale(holandes, (largura_hol, altura_hol))

player_image1 = pygame.image.load('imagens/bob_esponja_com_rede.png').convert_alpha()
player_image1 = pygame.transform.scale(player_image1, (largura_player, altura_player))

gary_image = pygame.image.load('imagens/gary.png').convert_alpha()
gary_image = pygame.transform.scale(gary_image, (largura_agua_viva, altura_agua_viva))

player_image2 = pygame.image.load('imagens/patrick_com_rede.png').convert_alpha()
player_image2 = pygame.transform.scale(player_image2, (largura_player, altura_player))

background_pontuacao = pygame.image.load('imagens/1_tela_pontuacao.png').convert_alpha()
background_pontuacao = pygame.transform.scale(background_pontuacao, (WIDTH, HEIGHT))

IMAGEM_CERTA = pygame.image.load('imagens/tela_entrada.png').convert()
IMAGEM_CERTA = pygame.transform.scale(IMAGEM_CERTA,(WIDTH,HEIGHT))

# Carrega os sons do jogo
pygame.mixer.music.set_volume(0.4)
musica = pygame.mixer.Sound('musica.mp3')
som_agua_viva = pygame.mixer.Sound('somag.mp3')
boom = pygame.mixer.Sound('boom.mp3')
heheheha = pygame.mixer.Sound('heheheha.mp3')
sominicio = pygame.mixer.Sound('sominicio.mp3')
som_gary = pygame.mixer.Sound('garysom.mp3')
sominicio.set_volume(0.2)
bobganha = pygame.mixer.Sound('bobganha.mp3')

# ----- Inicia estruturas de dados
game = True
score1 = 0
score2 = 0
tempo_gary = 0

# Carregar o dicionário de jogadores existente do arquivo JSON, se houver
try:
    with open("players.json", "r") as file:
        players = json.load(file)
except FileNotFoundError:
    players = {}
    

'''a abstração  inicial foi feita nas três classes abaixo, que compartilhavam 
as mesmas funções init e update, portanto, julgou-se necessário, visando a melhoria do código
- em pontos de leitura, manutenção e simplificação - a abstração desta parte.
'''

class ObjetosMoveis(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = imgagens
        self.rect = pygame.Rect(0, 0, largura_agua_viva, altura_agua_viva)
        self.rect.x = random.randint(-100,-50)
        self.rect.bottom = random.randint(0, HEIGHT-100)
        self.speedx = random.randint(2, 6)
        self.speedy = 0
    
    def update(self):
        # Atualizando a posição do objeto
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Se o objeto passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.left > WIDTH:
            self.rect.x = -100
            self.rect.bottom = random.randint(0, HEIGHT-100)
            self.speedx = random.randint(2, 6)
            self.speedy = 0

class AGUA_VIVA(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        super().__init__(self, imgagens, largura_agua_viva, altura_agua_viva, 2,6 )

class GARY(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        super().__init__(self, imgagens, largura_agua_viva, altura_agua_viva, 2,6 )

class HOLANDES(pygame.sprite.Sprite):
    def __init__(self, imgagens):
        super().__init__(self, imgagens, largura_hol, altura_hol, 2,6 )


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
            self.speedy = -5
            self.speedx = 0
        elif keys[self.keys['down']]:
            self.speedy = 5
            self.speedx = 0
        else:
            self.speedy = 0

        if keys[self.keys['left']]:
            self.speedx = -5
            self.speedy = 0
        elif keys[self.keys['right']]:
            self.speedx = 5
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

def tela_tutorial(BOTAOCLICADO):
    BOTAOCLICADO = False
    executando1 = True
    enter_text = fonte.render("aperte enter para jogar", True, (PRETO))
    while executando1:
        window.blit(Tela_tutorial,(0,0))
        window.blit(enter_text,(125,550))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando1 = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    BOTAOCLICADO = True
                    return BOTAOCLICADO
        pygame.display.update()
        

# ----- Criação de objetos
player1 = Player(player_image1, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d})
player2 = Player(player_image2, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT})


all_holandeses = pygame.sprite.Group()
all_aguas_vivas = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_gary = pygame.sprite.Group()

# Adiciona jogadores ao grupo de sprites
all_sprites.add(player1)
player1.rect.centerx = WIDTH / 3
player1.rect.bottom = HEIGHT - 8

all_sprites.add(player2)
player2.rect.centerx = WIDTH / 2
player2.rect.bottom = HEIGHT - 12


screen_uptdate_cout = 0

for i in range(6):
    agua_viva1 = AGUA_VIVA(agua_viva_small)
    all_aguas_vivas.add(agua_viva1)

if level == 0 or level==1:
    for i in range(2):
        tubarao = HOLANDES(hoandes_grande)
        all_holandeses.add(holandes)

if level == 2:
    for i in range(3):
        tubarao = HOLANDES(hoandes_grande)
        all_holandeses.add(holandes)


for i in range(1):
    gary = GARY(gary_image)
    all_gary.add(gary)

clock = pygame.time.Clock()
FPS = 60
i=0
pygame.display.set_caption("Jelly Jumble")

# Variável para verificar se o botão está pressionado em Pygame
botao_clicado = False
nomes_colocados = 0
nomes_jogadores = []
#loop da tela de entrada
executando = True
while executando:
    sominicio.play()
    screen_uptdate_cout += 1 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # Quando o jogador pressionar Enter, adicionar o nome e pontuação ao dicionário de jogadores
                nomes_jogadores.append(player_name)
                nomes_colocados += 1
                if player_name:
                    with open("players.json", "r") as file:
                        conteudo = file.read()
                    dados = json.loads(conteudo)
                    for player in dados:
                        if player == player_name:
                            player_score = dados[player]
                    if player_name not in dados:
                        dados[player_name] = 0
                    with open("players.json", "w") as file:
                        json.dump(dados, file)
                    player_name = ""
                if nomes_colocados == 2:
                    nomes_colocados = 0
                    botao_clicado = tela_tutorial(botao_clicado)
            elif evento.key == pygame.K_BACKSPACE:
                # Quando o jogador pressionar Backspace, remover o último caractere do nome
                player_name = player_name[:-1]
            elif evento.key == pygame.K_UP:
                # Quando o jogador pressionar a seta para cima, aumentar a pontuação
                player_score += 1
            elif evento.key == pygame.K_DOWN:
                # Quando o jogador pressionar a seta para baixo, diminuir a pontuação (mínimo de 0)
                player_score = max(0, player_score - 1)
            else:
                # Adicionar o caractere digitado ao nome do jogador
                player_name += evento.unicode

    # Desenha o botão em Pygame
    window.blit(IMAGEM_CERTA,(0,0))

    if nomes_colocados == 0:
        text = fonte.render("Nome do jogador 1: " + player_name, True, PRETO)

    elif nomes_colocados == 1:
        text = fonte.render("Nome do jogador 2: " + player_name, True, PRETO)

    text_rect = text.get_rect(center=(300, 550))
    window.blit(text, text_rect)

    if not botao_clicado:
        pygame.display.update()
    else:
        pygame.mixer.stop()
        nome_jogador1 = nomes_jogadores[0]
        nome_jogador2 = nomes_jogadores[1]
        clock = pygame.time.Clock()
        #atualiza a tela 60 vezes por segundo
        FPS = 60
        current_time = 0
        tempo = 0
        start_time = time.time()
        time_started = False
        tempo_restante = 0

        # ===== Loop principal =====
        musica.play()
        while game:
            clock.tick(FPS)

            current_time = time.time() - start_time
            
            if current_time>=1 and not time_started:
                time_started = True
                start_time = time.time()
            
            if current_time >= 30 and current_time<=45:
                level = 1
            elif current_time >= 45:
                level = 2
            # ----- Trata eventos
            for event in pygame.event.get():
                # ----- Verifica consequências
                if event.type == pygame.QUIT:
                    game = False

            # ----- Atualiza estado do jogo
            all_sprites.update()


            # Verifica colisão entre os jogadores e os obstáculos
            if pygame.sprite.spritecollide(player1, all_tubaroes, False):
                boom.play()
                heheheha.play()
                player1.rect.centerx = WIDTH / 3
                player1.rect.bottom = HEIGHT - 8
                score1 = 0

            if pygame.sprite.spritecollide(player2, all_tubaroes, False):
                boom.play()
                heheheha.play()
                player2.rect.centerx = WIDTH / 2
                player2.rect.bottom = HEIGHT - 15
                score2 = 0
            
            if pygame.sprite.spritecollide(player1, all_aguas_vivas, True):
                som_agua_viva.play()
                score1 += 1
                agua_viva1 = AGUA_VIVA(agua_viva_small)
                all_aguas_vivas.add(agua_viva1)

            if pygame.sprite.spritecollide(player2, all_aguas_vivas, True):
                som_agua_viva.play()
                score2 += 1
                agua_viva1 = AGUA_VIVA(agua_viva_small)
                all_aguas_vivas.add(agua_viva1)

            if pygame.sprite.spritecollide(player1, all_gary, True):
                som_gary.play()
                score1 += 4

            if pygame.sprite.spritecollide(player2, all_gary, True):
                som_gary.play()
                score2 += 4
                
            tempo_gary += clock.get_time() / 1000  # Converte o tempo para segundos

            # Verifica se é hora de criar um novo Gary
            if tempo_gary >= 15:
                gary = GARY(gary_image)
                all_gary.add(gary)
                tempo_gary = 0  # Reinicia o contador de tempo para a próxima aparição do Gary

            for tubarao in all_holandeses:
                tubarao.update()
            
            for aguaviva in all_aguas_vivas:
                aguaviva.update()

            for gary in all_gary:
                gary.update()

            # ----- Gera saídas
            window.fill((0, 0, 0))  # Preenche com a cor preta
            window.blit(background, (0, 0))
            all_holandeses.draw(window)
            all_aguas_vivas.draw(window)
            all_gary.draw(window)
            all_sprites.draw(window)
            

            # Exibe a pontuação na tela
            score1_text = fonte.render(f"{nome_jogador1}: " + str(score1), True, (BRANCO))
            window.blit(score1_text, (10, 10))
            score2_text = fonte.render(f"{nome_jogador2}: " + str(score2), True, (BRANCO))
            window.blit(score2_text, (10, 50))


            if time_started:

                tempo_restante = 60-current_time
                tempo_text = fonte.render("Tempo restante: {0:.0f}".format((tempo_restante)), True, (255,255,255))
                window.blit(tempo_text, (270, 10)) 

                if current_time >= 60:
                    game = False
                    executando = False

                elif current_time >= 20 and i ==1:
                    tubarao = HOLANDES(hoandes_grande)
                    all_holandeses.add(tubarao)
                    i+=1

            pygame.display.update()

#atualiza arquivo com as pontuacoes
with open('players.json', 'r') as file:
    conteudo = file.read()
dados = json.loads(conteudo)
for player in dados:
    if player == nome_jogador1:
        if score1 > dados[nome_jogador1]:
            dados[nome_jogador1] = score1
    elif player == nome_jogador2:
        if score2 > dados[nome_jogador2]:
            dados[nome_jogador2] = score2

ranking = {}
current = 100000000
for i in range(5):
    high_score = 0
    for player in dados:
        pontuacao = dados[player]
        if pontuacao > high_score and pontuacao < current:
            high_score = pontuacao
            best_player = player
    ranking[best_player] = high_score
    current = high_score

best_players = []
for player in ranking:
    best_players.append(player)

best_pontuacoes = []
for pontuacao in ranking.values():
    best_pontuacoes.append(pontuacao)

with open('players.json', 'w') as file:
    json.dump(dados, file)

pygame.mixer.stop()
tela_final = True
bobganha.play()

def Ranking():
    highscore_text = fonte.render("Top 5 players:", True, (PRETO))
    X = 200
    Y = 130
    window.blit(highscore_text, (X, Y))
    e = 50
    for i in range (len(best_players)):
        bestplayer_text = fonte.render(f"{best_players[i]}", True, (PRETO))
        bestpontuacoes_text = fonte.render(f"{best_pontuacoes[i]}", True, (PRETO))
        window.blit(bestplayer_text, (X, Y+e))
        window.blit(bestpontuacoes_text, (X+200, Y+e))
        e += 50

def pontuacoes_partida():
    pontuacao1_text = fonte.render(f"Pontos {nome_jogador1}: {score1}", True, (PRETO))
    pontuacao2_text = fonte.render(f"Pontos {nome_jogador2}: {score2}", True, (PRETO))
    window.blit(pontuacao1_text, (10, 490))
    window.blit(pontuacao2_text, (10, 540))

while tela_final:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            tela_final = False

    '''possível abstração nesses tres ultimos???''' 

    if score1>score2:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        bob_text = fonte.render(f"{nome_jogador1} venceu! ", True, (PRETO))
        pontuacao1_text = fonte.render(f"Pontos {nome_jogador1}: {score1}", True, (PRETO))
        pontuacao2_text = fonte.render(f"Pontos {nome_jogador2}: {score2}", True, (PRETO))
        window.blit(background_pontuacao, (0,0)) 
        window.blit(bob_text, (170, 30))
        pontuacoes_partida()
        Ranking()

                        
    elif score2>score1:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        pat_text = fonte.render(f"{nome_jogador2} venceu! ", True, (PRETO))
        window.blit(background_pontuacao, (0,0))
        window.blit(pat_text, (170, 30))
        pontuacoes_partida()
        Ranking()
     
    else:
        window.fill((0, 0, 0))  # Preenche com a cor preta
        holandes_text = fonte.render("EMPATE", True, (PRETO))
        window.blit(background_pontuacao, (0,0))
        window.blit(holandes_text, (220, 30))
        pontuacoes_partida()
        Ranking()

    pygame.display.update()