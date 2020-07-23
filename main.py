import time
import random
import pygame

from background import Background
from sprite import Player, Enemy, Buoy, FinishLine

pygame.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Boating Game")

# time related
clock = pygame.time.Clock()
TOTAL_GAME_TIME = remaining_game_time = 30  # seconds
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)


# miscellaneous
font = pygame.font.SysFont("Consolas", 150)


def redraw_window():
    background.update(win)

    buoy1.update(win)  # should be behind the boat

    finish_line.update(win)

    player.update(win)
    enemy.update(win)

    buoy2.update(win)  # should be in front the boat

    pygame.display.update()


def draw_text(text, x, y):
    background.update(win)

    player.update_once(win)
    enemy.update_once(win)

    win.blit(font.render(text, True, (0, 0, 0)), (x, y))

    pygame.display.update()


background = Background(image="backgrounds/rsz_bg.jpg")
player = Player(x=0, y=550, speed=5, image_dir="sprites/team1/")
enemy = Enemy(x=0, y=650, speed=15, image_dir="sprites/team2/")
buoy1 = Buoy(x=WIDTH + 100, y=610, speed=0, image="sprites/buoyo.png")
buoy2 = Buoy(x=WIDTH + 100, y=740, speed=0, image="sprites/buoyo.png")
finish_line = FinishLine(
    x1=WIDTH + 100 + buoy1.image.get_width() / 2,
    y1=610 + 50,
    x2=WIDTH + 100 + buoy1.image.get_width() / 2,
    y2=740 + 40,
)

# pregame countdown
for t in range(3, 0, -1):
    draw_text(str(t), x=WIDTH / 2, y=HEIGHT / 2)
    time.sleep(1)

# actual game
running = True
while running:
    clock.tick(30)  # FPS

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.USEREVENT:
            remaining_game_time -= 1

        if event.type == pygame.USEREVENT + 1:
            enemy.x += enemy.speed

            # randomize time to update USEREVENT+1; results in random speed boosts for enemy
            update_time = random.randint(400, 600)
            pygame.time.set_timer(pygame.USEREVENT + 1, update_time)

    # handle time and speeds of objects
    if remaining_game_time >= TOTAL_GAME_TIME * 0.25:
        # scroll background at normal speed
        background.scroll(speed=background.bg_speed)

        # by default, sprites should move faster than the background due to paddling action
        player.x -= background.bg_speed / 2
        enemy.x -= background.bg_speed / 2

    else:
        # if near the end of the race, sprites are half-way through the screen,
        # start scrolling faster
        if (
            player.x + player.spritesheet[0].get_width() > WIDTH / 2
            or enemy.x + enemy.spritesheet[0].get_width() > WIDTH / 2
        ):
            # speed up background scrolling
            background.scroll(speed=background.bg_speed * 1.2)

            # speed up buoy + finish line movement
            buoy1.speed = background.bg_speed * 1.2
            buoy2.speed = background.bg_speed * 1.2
            finish_line.speed = background.bg_speed * 1.2

        else:
            # stop background scrolling if sprites are not half-way
            background.scroll(speed=0)

            # move buoys + finish line with the background
            buoy1.speed = background.bg_speed
            buoy2.speed = background.bg_speed
            finish_line.speed = background.bg_speed

            # after background stops scrolling (towards the end of the race),
            # sprites should have +ve velocity when "idling" (no keyboard input)
            player.x += 2
            enemy.x += 2

    playerposition = finish_line.x1 - (
        player.x + player.spritesheet[0].get_width() - 10
    )
    enemyposition = finish_line.x1 - (enemy.x + enemy.spritesheet[0].get_width() - 10)
    if playerposition < 0 or enemyposition < 0:
        time.sleep(1)

        if playerposition < enemyposition:
            text = "YOU WON!"
            draw_text(text, x=WIDTH / 2 - 300, y=HEIGHT / 2)
        else:
            text = "WHAT A LOSER"
            draw_text(text, x=WIDTH / 2 - 400, y=HEIGHT / 2)

        time.sleep(1)

        pygame.quit()
        break

    redraw_window()
