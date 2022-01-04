import time

import pygame
from Class import Player, Enemy

# Init pygame
pygame.init()
clock = pygame.time.Clock()

# Set game window size (should be resizable)
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
game_round = 0
max_rounds = 11
score = 0
death_zone = dimension - (dimension / 5)
retry = True
victory = False

# ------- Creating player object
x = dimension / 2
y = dimension - (dimension / 10)
player = Player(background, x, y, dimension, dimension / 20)

# ------- Creating bullet related variables
shooting = False
bullet_y = 0
bullet_x = 0
bullet_speed = dimension / 50  # Smaller means faster

# ------- Creating enemies and related variables
enemies = []
enemyStep = 0
enemyStepMax = dimension / 10
enemyDirection = "LEFT"
down = False
down_count = 0


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


# Start menu
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


# Game over menu
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
                    game_round = 0
                    score = 0
                    running = True
                    game_lost = False
                elif event.key == pygame.K_ESCAPE:
                    retry = False
                    game_lost = False

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


# Main game loop
def main():
    global running, shooting, bullet_y, bullet_x, enemyStep, enemyDirection, score, game_round, enemyStepMax, down, down_count, max_rounds, victory

    while running:

        # (Re)draw background
        background.fill((0, 0, 0))

        # Handle on screen info
        font = pygame.font.SysFont(None, 48)

        text = font.render("Round: " + str(game_round - 1) + "/" + str(max_rounds - 1), True, (200, 200, 200))
        text_rect = text.get_rect(center=(100, 30))

        score_text = font.render("Score: " + str(score), True, (200, 200, 200))
        score_text_rect = score_text.get_rect(center=(100, 80))

        tuto = font.render("Shoot: UP", True, (200, 200, 200))
        tuto_rect = tuto.get_rect(center=(dimension - (dimension / 10), 30))

        background.blit(text, text_rect)
        background.blit(score_text, score_text_rect)
        background.blit(tuto, tuto_rect)

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
                enemy_moved = enemy.move(enemyDirection, down)

                # Game over
                if enemy.y >= death_zone:
                    running = False

                enemyDirection = enemy_moved[0]
                down = enemy_moved[1]

                if down and down_count != game_round - 1:
                    down_count = game_round - 1

                # Enemy death
                if (enemy.x - enemy.radius) <= bullet_x <= (enemy.x + enemy.radius) and (
                        enemy.y - enemy.radius) <= bullet_y <= (enemy.y + enemy.radius):
                    score += enemy.enemy_id * game_round
                    enemies.remove(enemy)
                    hit.play()
                    bullet_y = -dimension

                down_count -= 1

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
                victory = True
                running = False
            else:
                game_round += 1
                enemyStepMax = enemyStepMax * game_round * 2
                create_mobs()

        # Update display
        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def win():
    global background, dimension, running, game_round, score, retry

    pygame.mixer.music.load('Assets/victory.mp3')
    pygame.mixer.music.play(-1, 0.0)

    font = pygame.font.SysFont(None, 48)

    text = font.render("YOU WON!!!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(dimension / 2, dimension / 2))

    screen.blit(text, text_rect)
    background.fill((255, 255, 255))
    pygame.display.update()

    text = font.render("Press SPACE to replay or ESCAPE to quit", True, (255, 255, 255))
    text_rect = text.get_rect(center=(dimension / 2, dimension / 1.5))

    screen.blit(text, text_rect)
    background.fill((255, 255, 255))
    pygame.display.update()

    game_won = True
    while game_won:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_round = 0
                    score = 0
                    running = True
                    game_won = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


menu()
pygame.mixer.music.play(-1, 0.0)
while retry:
    main()
    if victory:
        win()
    print("Retry")
    enemies = []
    game_round = 1
    create_mobs()
    lose()

pygame.quit()
