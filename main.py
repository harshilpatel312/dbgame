import pygame

pygame.init()

win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

bg = pygame.image.load('riverbg.jpg')
bgX = 0
bgX2 = bg.get_width()


player_sprites = [pygame.image.load('sprites/boat1.png'), pygame.image.load('sprites/boat2.png'), 
                  pygame.image.load('sprites/boat3.png'), pygame.image.load('sprites/boat4.png'), 
                  pygame.image.load('sprites/boat5.png'), pygame.image.load('sprites/boat6.png'), 
                  pygame.image.load('sprites/boat7.png'), pygame.image.load('sprites/boat8.png'), 
                  pygame.image.load('sprites/boat9.png'), pygame.image.load('sprites/boat10.png'), 
                  pygame.image.load('sprites/boat11.png'), pygame.image.load('sprites/boat12.png')]

sprite1 = [pygame.transform.scale(x, (250, 163)) for x in player_sprites]

def redraw_window(x, y):
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    win.blit(sprite1[frame//2], (x, y))

    pygame.display.update()

speed = 30
frame = 0
running = True
score = 0

playerx = 40
playery = 550
playerspeed = 5

while running:
    redraw_window(playerx, playery)

    playerx -= 0.7 # by default, player should move a little faster than the background 
    bgX -= 1.4
    bgX2 -= 1.4

    # so that player doesn't go out of screen
    if playerx < 0:
        playerx = 0
        
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
            playerx += playerspeed
            score += 1
            print("+1", frame, score)

        if frame > 8:
            playerx += -playerspeed+2
            score -= 1
            print("-1", frame, score)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(speed)
