import time

import pygame
from Class import Player, Enemy

# Init pygame
pygame.init()
clock = pygame.time.Clock()

# Set game window size (not customizable yet)
dimension = 2000

# Create game window and canvas
screen = pygame.display.set_mode((dimension, dimension))
background = pygame.Surface((dimension, dimension))

# Set game explicit properties
pygame.display.set_caption("Nispace Invader 3000")
image = pygame.image.load("Assets/logo.png").convert()
pygame.display.set_icon(image)

# Set up sounds
pygame.mixer.music.load('Assets/nispace_invader.mp3')
hit = pygame.mixer.Sound('Assets/Hit.mp3')

# Set up all necessary variables
running = True
game_round = 1
max_rounds = 10
score = 0
death_zone = dimension - (dimension / 5)
retry = True

# ------- Creating player object
x = dimension / 2
y = dimension - (dimension / 10)
player = Player(background, x, y, dimension, dimension / 20)

# ------- Creating bullet related variables
shooting = False
bullet_y = 0
bullet_x = 0
bullet_speed = dimension / 50  # Smaller means faster

# ------- Creating enemies
enemies = []
enemyStep = 0
enemyStepMax = dimension / 10
enemyDirection = "LEFT"


def create_mobs():

    i = 1
    x_pos = 1
    on_row = 0
    row = 1
    while i < game_round:
        if on_row == 4:
            row += 1
            on_row = 0
            x_pos = 1

        enemies.append(
            Enemy(i, background, ((dimension / 10) * x_pos * 2), ((dimension / 10) * row), dimension, dimension / 20))
        on_row += 1
        x_pos += 1
        i += 1


intro = True


def menu():
    global intro, background, dimension

    font = pygame.font.SysFont(None, 48)

    text = font.render("Press any key to start the game", True, (200, 200, 200))
    text_rect = text.get_rect(center=(dimension / 2, dimension / 2))

    screen.blit(text, text_rect)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                intro = False
        background.fill((255, 255, 255))
        pygame.display.update()
        clock.tick(15)


def lose():
    global background, dimension, running, game_round, score, retry

    font = pygame.font.SysFont(None, 48)

    text = font.render("YOU LOST", True, (255, 0, 0))
    text_rect = text.get_rect(center=(dimension / 2, dimension / 2))

    screen.blit(text, text_rect)
    background.fill((255, 255, 255))
    pygame.display.update()

    text = font.render("Press SPACE to retry or ESCAPE to quit", True, (255, 0, 0))
    text_rect = text.get_rect(center=(dimension / 2, dimension / 1.5))

    screen.blit(text, text_rect)
    background.fill((255, 255, 255))
    pygame.display.update()

    game_lost = True
    while game_lost:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_round = 1
                    score = 0
                    running = True
                    game_lost = False
                elif event.key == pygame.K_ESCAPE:
                    retry = False
                    game_lost = False

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


# Game loop
def main():
    global running, shooting, bullet_y, bullet_x, enemyStep, enemyDirection, score, game_round, enemyStepMax

    while running:

        # (Re)draw background
        background.fill((0, 0, 0))

        # Place player and yellow shield
        player.create()
        pygame.draw.rect(background, (255, 255, 0), pygame.Rect(0, death_zone, dimension, dimension / 100))

        # Place enemies
        for enemy in enemies:
            enemy.create()

        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # If LEFT or RIGHT then player move
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move(event.key)

                # If UP then player shoot
                if event.key == pygame.K_UP:
                    if not shooting:
                        bullet_x = player.x
                        bullet_y = player.y
                        shooting = True

                # If ESCAPE then close game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Handle bullet trajectory if one is currently on screen
        if shooting:
            bullet_y -= bullet_speed
            bullet = pygame.draw.circle(background, (0, 255, 255), (bullet_x, bullet_y), 20)

            if bullet_y <= 0:
                shooting = False

        # Handle enemy movements
        if enemyStep < enemyStepMax:
            for enemy in enemies:
                enemyDirection = enemy.move(enemyDirection)
                if (enemy.x - enemy.radius) <= bullet_x <= (enemy.x + enemy.radius) and (
                        enemy.y - enemy.radius) <= bullet_y <= (enemy.y + enemy.radius):
                    print("HIT!")
                    score += enemy.enemy_id
                    print("Score :" + str(score))
                    enemies.remove(enemy)
                    hit.play()
                    bullet_y = -dimension
        elif enemyStep >= enemyStepMax:
            for enemy in enemies:
                enemy.move('DOWN')
                if enemy.y >= death_zone:
                    running = False
            enemyStep = 0
            if enemyDirection == "LEFT":
                enemyDirection = "RIGHT"
            elif enemyDirection == "RIGHT":
                enemyDirection = "LEFT"
        enemyStep += 1

        # Increase rounds
        if not enemies:
            if game_round >= max_rounds:
                print("YOU WON!")
                running = False
            else:
                game_round += 1
                enemyStepMax = enemyStepMax * game_round * 2
                create_mobs()

        # Update display
        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)


menu()
pygame.mixer.music.play(-1, 0.0)
while retry:
    main()
    print("Retry")
    enemies = []
    create_mobs()
    lose()

pygame.quit()
