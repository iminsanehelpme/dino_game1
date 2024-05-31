import pygame 
import random
import math

# Creazione di variabili utili e creazione schermo
pygame.init()
screen = pygame.display.set_mode((1080, 720))

dino1 = pygame.image.load("ImmaginiGioco/Dino1.png")
dino2 = pygame.image.load("ImmaginiGioco/Dino2.png")
ground = pygame.image.load("ImmaginiGioco/ground.png")
cactus = pygame.image.load("ImmaginiGioco/Cactus.png")
nuvola = pygame.image.load("ImmaginiGioco/Nuvola.png")
game_font = pygame.font.Font("ImmaginiGioco/PressStart2P-Regular.ttf", 24)

clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

# Gestione generale del gioco
game_over = False
running = True
spacing = 18
score = 0
best = 0

# Variabili animazione salto
salto = -48
ydino = 370

# Variabili animazione corsa
velocità = -40
scroll = 0

# Spessore immagine ground
bg_width = ground.get_width()
tiles = math.ceil(1080 / bg_width) + 2

# Generazione cactus
prob = 1 / 2
cactuses = []
tick = 100

# Generazione nuvole
clouds = []

# Funzione per visualizzare la schermata di game over
def show_game_over():
    game_over_text = game_font.render("G A M E  O V E R", True, (0, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Pulsante Restart
    restart_text = game_font.render("RESTART", True, (0, 0, 0))
    restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 25))
    pygame.draw.rect(screen, (200, 200, 200), restart_rect.inflate(20, 10))
    screen.blit(restart_text, restart_rect)

    # Pulsante Quit
    quit_text = game_font.render("QUIT", True, (0, 0, 0))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 75))
    pygame.draw.rect(screen, (200, 200, 200), quit_rect.inflate(20, 10))
    screen.blit(quit_text, quit_rect)

    return restart_rect, quit_rect

while True:
    while running:
        game_over_text = ''
        # Stampa sfondo
        screen.fill('white')
        for i in range(0, tiles):
            screen.blit(ground, (i * bg_width + scroll, 475))

        # Spawn recta cactus
        x_cactus = 1080
        if tick % spacing == 0 and random.random() < prob:
            Dx = random.randint(1, 3)
            for i in range(Dx):
                cactuses.append([cactus, x_cactus - (25 * (Dx - 1)), 426, 0])
                x_cactus += 50
        for i in cactuses:
            i[1] += velocità
            screen.blit(i[0], (i[1], i[2]))
            if i[1] <= 35 and i[3] == 0:
                i[3] = 1
                score += 1

        # Spawn nuvole
        x_cloud = 1080
        if tick % (spacing * 8) == 0:
            clouds.append([nuvola, x_cloud, random.randint(150, 300)])
        for i in clouds:
            i[1] += velocità / 8
            screen.blit(i[0], (i[1], i[2]))

        # Animazione corsa
        if (tick // 4) % 2 == 0:
            screen.blit(dino1, (35, ydino))
        else:
            screen.blit(dino2, (35, ydino))

        # Controllo input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif (event.type == pygame.KEYDOWN) and (event.unicode in (' ', 'w')) and (salto < -48):
                salto = -velocità * 1.2
        if salto >= -48:
            ydino -= salto
            salto -= 8

        # Scroll background
        scroll += velocità
        if abs(scroll) > bg_width:
            scroll = 0

        # collisione
        for i in cactuses:
            if 35 <= i[1] <= 112 and ydino >= 345:
                velocità = 0
                tick = 0
                game_over = True
                running = False

        # Progresso corsa
        tick -= velocità / 40
        clock.tick(math.pow(tick, 0.5))
        screen.blit(game_font.render("Score: "+str(score),True,(0,0,0)),(800,50))
        screen.blit(game_font.render("Best: "+str(best),True,(0,0,0)),(800,100))
        pygame.display.update()

    # Mostra la schermata di game over
    restart_rect, quit_rect = show_game_over()
    pygame.display.update()

    # Gestione input nella schermata di game over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    # Riavvia il gioco
                    game_over = False
                    running = True
                    if score > best:
                        best = score
                    score = 0
                    cactuses = []
                    clouds = []
                    velocità = -40
                    scroll = 0
                    salto = -48
                    ydino = 370
                    floor = -48
                    tick = 100
                elif quit_rect.collidepoint(event.pos):
                    # Esci dal gioco
                    game_over = False
                    pygame.quit()
