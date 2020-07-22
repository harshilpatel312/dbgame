import pygame
import random
from sprite import Player, Enemy

pygame.init()

win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("First Game")

# time related
clock = pygame.time.Clock()
game_time = 30  # seconds
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

bg = pygame.image.load("backgrounds/rsz_bg.jpg")
bgX = 0
bgX2 = bg.get_width()
font = pygame.font.SysFont("Consolas", 30)


def redraw_window():
    win.blit(bg, (bgX, 0))
    win.blit(pygame.transform.flip(bg, True, False), (bgX2, 0))

    if game_time <= 3:
        win.blit(font.render(str(game_time), True, (0, 0, 0)), (32, 48))

    player.update(win)
    enemy.update(win)

    pygame.display.update()


speed = 30
frame = 0
running = True

player = Player(x=0, y=550, speed=5, image_dir="sprites/team1/")
enemy = Enemy(x=0, y=650, speed=15, image_dir="sprites/team2/")

while running:
    clock.tick(speed)

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
    if game_time > 10:  # stop background scrolling towards the end of the race
        bgX -= 1.4
        bgX2 -= 1.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()

        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        # by default, sprites should move faster than the background due to paddling action
        player.x -= 0.7
        enemy.x -= 0.7
    else:
        # after background stops scrolling (towards the end of the race), sprites should have +ve velocity when there's no keyboard input (space bar)
        player.x += 2
        enemy.x += 2

    if game_time == 0:
        pygame.quit()
        break

    redraw_window()
