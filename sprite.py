import pygame


class Sprite:
    def __init__(self, x, y, speed, image_dir):
        self.x = x
        self.y = y
        self.speed = speed
        self.spritesheet = [
            pygame.transform.scale(
                pygame.image.load("{}boat{}.png".format(image_dir, image)),  # FIXME
                (250, 163),
            )
            for image in range(1, 13)
        ]

        self.score = 0
        self.spriteframe = 0

    def update(self, screen):
        if self.spriteframe + 1 >= 24:
            self.spriteframe = 0
        self.spriteframe += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.spriteframe > 0 and self.spriteframe <= 8:
                self.x += self.speed
                self.score += 1
                print("+1", self.spriteframe, self.score)

            if self.spriteframe > 8:
                self.x += -self.speed + 2
                self.score -= 1
                print("-1", self.spriteframe, self.score)

        screen.blit(self.spritesheet[self.spriteframe // 2], (self.x, self.y))
