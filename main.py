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


def redraw_window(x, y):
    win.blit(bg, (bgX, 0))
    win.blit(pygame.transform.flip(bg, True, False), (bgX2, 0))
    win.blit(player.spritesheet[frame // 2], (x, y))

    if game_time <= 3:
        win.blit(font.render(str(game_time), True, (0, 0, 0)), (32, 48))

    pygame.display.update()


speed = 30
frame = 0
running = True

player = Sprite(image_dir="sprites")
player.x = 40
player.y = 550
player.speed = 5

while running:
    redraw_window(player.x, player.y)

    player.x -= (
        0.7  # by default, player should move a little faster than the background
    )
    bgX -= 1.4
    bgX2 -= 1.4

    # so that player doesn't go out of screen
    if player.x < 0:
        player.x = 0

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    if frame + 1 >= 24:
        frame = 0
    frame += 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if frame > 0 and frame <= 8:
            player.x += player.speed
            player.score += 1
            print("+1", frame, player.score)

        if frame > 8:
            player.x += -player.speed + 2
            player.score -= 1
            print("-1", frame, player.score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.USEREVENT:
            game_time -= 1

    if game_time == 0:
        pygame.quit()

    clock.tick(speed)
