import pygame


class Sprite:
    def __init__(self, image_dir):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.score = 0
        self.spritesheet = [
            pygame.transform.scale(
                pygame.image.load("{}/boat{}.png".format(image_dir, image)), (250, 163)
            )
            for image in range(1, 13)
        ]
