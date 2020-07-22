import pygame
import random
from sprite import Player, Enemy

pygame.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Boating Game")

# time related
clock = pygame.time.Clock()
TOTAL_GAME_TIME = game_time = 30  # seconds
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

# background related
bg = pygame.image.load("backgrounds/rsz_bg.jpg")
bgX = 0
bgX2 = bg.get_width()
BG_SPEED = 1.4

# miscellaneous
font = pygame.font.SysFont("Consolas", 30)


def redraw_window():
    win.blit(bg, (bgX, 0))
    win.blit(pygame.transform.flip(bg, True, False), (bgX2, 0))

    if game_time <= 3:
        win.blit(font.render(str(game_time), True, (0, 0, 0)), (32, 48))

    player.update(win)
    enemy.update(win)

    pygame.display.update()


player = Player(x=0, y=550, speed=5, image_dir="sprites/team1/")
enemy = Enemy(x=0, y=650, speed=15, image_dir="sprites/team2/")

running = True
while running:
    clock.tick(30)  # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.USEREVENT:
            game_time -= 1

        if event.type == pygame.USEREVENT + 1:
            enemy.x += enemy.speed
            print("speeding up", enemy.x)

            # randomize time to update USEREVENT+1; results in random speed boosts for enemy
            update_time = random.randint(400, 600)
            pygame.time.set_timer(pygame.USEREVENT + 1, update_time)

    # handle background scrolling
    if (
        game_time < TOTAL_GAME_TIME * 0.25
    ):  # stop background scrolling towards the end of the race
        # after background stops scrolling (towards the end of the race),
        # sprites should have +ve velocity when "idling" (no keyboard input)
        player.x += 2
        enemy.x += 2

        # if after stopping background scrolling, player or enemy is
        # more than half-way through the screen, start scrolling again
        if (
            player.x + player.spritesheet[0].get_width() > WIDTH / 2
            or enemy.x + player.spritesheet[0].get_width() > WIDTH / 2
        ):
            bgX -= BG_SPEED * 1.2
            bgX2 -= BG_SPEED * 1.2

            if bgX < bg.get_width() * -1:
                bgX = bg.get_width()

            if bgX2 < bg.get_width() * -1:
                bgX2 = bg.get_width()

    else:
        # scroll background before the end of the race
        bgX -= BG_SPEED
        bgX2 -= BG_SPEED

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()

        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        # by default, sprites should move faster than the background due to paddling action
        player.x -= BG_SPEED / 2
        enemy.x -= BG_SPEED / 2

    if game_time == 0:
        pygame.quit()
        break

    redraw_window()
