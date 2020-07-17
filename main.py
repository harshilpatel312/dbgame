import pygame

pygame.init()

win = pygame.display.set_mode((800, 576))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

sprite = [pygame.image.load('boat1.png'), pygame.image.load('boat2.png'), 
               pygame.image.load('boat3.png'), pygame.image.load('boat4.png'), 
               pygame.image.load('boat5.png'), pygame.image.load('boat6.png'), 
               pygame.image.load('boat7.png'), pygame.image.load('boat8.png'), 
               pygame.image.load('boat9.png'), pygame.image.load('boat10.png'), 
               pygame.image.load('boat11.png'), pygame.image.load('boat12.png')]

bg = pygame.image.load('riverbg.jpg')
bgX = 0
bgX2 = bg.get_width()

def redraw_window():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    win.blit(sprite[frame//2], (40, 390))

    pygame.display.update()

speed = 30
frame = 0
running = True
while running:
    redraw_window()
    clock.tick(speed)
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    
    if frame + 1 >= 24:
        frame = 0
    frame += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
