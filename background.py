import pygame


class Background:
    # scrolling background logic: https://www.youtube.com/watch?v=PjgLeP0G5Yw
    def __init__(self, image):
        self.bg = pygame.image.load(image)
        self.bg_x = 0  # position of first background image
        self.bg_x2 = self.bg.get_width()  # position of second background image
        self.bg_speed = 1.4

    def scroll(self, speed):
        # scroll background before the end of the race
        self.bg_x -= speed
        self.bg_x2 -= speed

        if self.bg_x < self.bg.get_width() * -1:
            self.bg_x = self.bg.get_width()

        if self.bg_x2 < self.bg.get_width() * -1:
            self.bg_x2 = self.bg.get_width()

    def update(self, screen):
        screen.blit(self.bg, (self.bg_x, 0))
        screen.blit(pygame.transform.flip(self.bg, True, False), (self.bg_x2, 0))
