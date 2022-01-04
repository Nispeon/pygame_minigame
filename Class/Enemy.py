import pygame


class Enemy:
    def __init__(self, enemy_id, background, x, y, maximum, radius):
        self.enemy_id = enemy_id
        self.background = background
        self.x = x
        self.y = y
        self.moveValue = maximum / 100
        self.moveValueDown = maximum / 10
        self.max = maximum - (maximum / 10)
        self.radius = radius

    def create(self):
        pygame.draw.circle(self.background, (255, 0, 0), (self.x, self.y), self.radius)

    def move(self, direction):

        if self.x <= 100:
            direction = "RIGHT"
            self.y += self.moveValueDown

        elif self.x >= self.max:
            direction = "LEFT"
            self.y += self.moveValueDown


        if direction == "RIGHT":
            self.x += self.moveValue
        elif direction == "LEFT":
            self.x -= self.moveValue

        return direction
