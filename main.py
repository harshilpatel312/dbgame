import time
import random
import pygame

from background import Background
from sprite import Player, Enemy, Buoy, FinishLine

pygame.init()

WIDTH, HEIGHT = 1200, 1000
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dragon Boating Game")

# time related
clock = pygame.time.Clock()
TOTAL_GAME_TIME = remaining_game_time = 30  # seconds
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 1, 800)


# miscellaneous
font = pygame.font.SysFont("Consolas", 150)
start = pygame.mixer.Sound("start.wav")
horn = pygame.mixer.Sound("horn.wav")
racemusic = pygame.mixer.music.load("race.wav")

# instantiate
background = Background(image="backgrounds/rsz_bg.jpg")
player = Player(x=0, y=675, speed=5, image_dir="sprites/team1/")
enemy1 = Enemy(x=0, y=550, speed=15, image_dir="sprites/team2/")
enemy2 = Enemy(x=0, y=800, speed=15, image_dir="sprites/team3/")
buoy1 = Buoy(x=WIDTH + 100, y=610, speed=0, image="sprites/buoyo.png")
buoy2 = Buoy(x=WIDTH + 100, y=910, speed=0, image="sprites/buoyo.png")
finish_line = FinishLine(
    x1=WIDTH + 100 + buoy1.image.get_width() / 2,
    y1=610 + 50,
    x2=WIDTH + 100 + buoy1.image.get_width() / 2,
    y2=910 + 40,
)


def redraw_window():
    background.update(win)

    buoy1.update(win)  # should be behind the boat

    finish_line.update(win)

    enemy1.update(win)
    player.update(win)
    enemy2.update(win)

    buoy2.update(win)  # should be in front the boat

    pygame.display.update()


def draw_text(text, x, y):
    background.update(win)

    buoy1.update(win)  # should be behind the boat

    finish_line.update(win)

    enemy1.update_once(win)
    player.update_once(win)
    enemy2.update_once(win)

    win.blit(font.render(text, True, (0, 0, 0)), (x, y))

    buoy2.update(win)  # should be in front the boat

    pygame.display.update()


# pregame countdown
start.play()
time.sleep(2)
for t in range(3, 0, -1):
    draw_text(str(t), x=WIDTH / 2, y=HEIGHT / 2)
    if t == 1:
        horn.play()
    time.sleep(1)

# actual game
pygame.mixer.music.play(-1)
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
            enemy1.x += enemy1.speed + random.randint(5, 10)
            enemy2.x += enemy2.speed + random.randint(5, 10)

    # handle time and speeds of objects
    if remaining_game_time >= TOTAL_GAME_TIME * 0.25:
        # scroll background at normal speed
        background.scroll(speed=background.bg_speed)

        # by default, sprites should move faster than the background due to paddling action
        player.x -= background.bg_speed / 2
        enemy1.x -= background.bg_speed / 2
        enemy2.x -= background.bg_speed / 2

    else:
        # if near the end of the race, sprites are half-way through the screen,
        # start scrolling faster
        if (
            player.x + player.spritesheet[0].get_width() > WIDTH / 2
            or enemy1.x + enemy1.spritesheet[0].get_width() > WIDTH / 2
            or enemy2.x + enemy2.spritesheet[0].get_width() > WIDTH / 2
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
            enemy1.x += 2
            enemy2.x += 2

    # check for game end
    playerposition = finish_line.x1 - (
        player.x + player.spritesheet[0].get_width() - 10
    )
    enemy1position = finish_line.x1 - (
        enemy1.x + enemy1.spritesheet[0].get_width() - 10
    )
    enemy2position = finish_line.x1 - (
        enemy2.x + enemy2.spritesheet[0].get_width() - 10
    )
    if playerposition < 0 or enemy1position < 0 or enemy2position < 0:
        time.sleep(0.5)
        pygame.mixer.music.stop()
        if playerposition < enemy1position and playerposition < enemy2position:
            text = "YOU WON!"
            draw_text(text, x=WIDTH / 2 - 300, y=HEIGHT / 2)
        else:
            text = "WHAT A LOSER"
            draw_text(text, x=WIDTH / 2 - 400, y=HEIGHT / 2)

        time.sleep(3)

        pygame.quit()
        break

    redraw_window()
