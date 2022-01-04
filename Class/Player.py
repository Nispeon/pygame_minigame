import pygame


class Player:
    def __init__(self, background, x, y, maximum, radius):
        self.background = background
        self.x = x
        self.y = y
        self.moveValue = maximum / 10
        self.max = maximum - self.moveValue
        self.radius = radius

    def create(self):
        pygame.draw.circle(self.background, (0, 0, 255), (self.x, self.y), self.radius)

    def move(self, key):
        if key == pygame.K_LEFT:
            if self.x > self.moveValue:
                self.x -= self.moveValue
        elif key == pygame.K_RIGHT:
            if self.x < self.max:
                self.x += self.moveValue

