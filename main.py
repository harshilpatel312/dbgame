import pygame
from sprite import Sprite

pygame.init()

win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("First Game")

# time related
clock = pygame.time.Clock()
game_time = 10  # seconds
pygame.time.set_timer(pygame.USEREVENT, 1000)

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

    pygame.display.update()


speed = 30
frame = 0
running = True

player = Sprite(x=40, y=550, speed=5, image_dir="sprites")

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.USEREVENT:
            game_time -= 1

    # handle background speed
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    # handle player
    player.x -= 0.7  # by default, player should move a little faster than the background due to paddling action

    if player.x < 0:
        player.x = 0

    if game_time == 0:
        pygame.quit()
        break

    redraw_window()
